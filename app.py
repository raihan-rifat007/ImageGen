import os
import base64
import time
import random
from urllib.parse import quote
from dataclasses import dataclass, field
from typing import Optional
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@dataclass(frozen=True)
class ProviderConfig:
    hf_key: str = os.getenv("HF_API_KEY", "")
    horde_key: str = os.getenv("HORDE_APIKEY", "0000000000")


@dataclass(frozen=True)
class GenerationParams:
    prompt: str
    negative: str = ""
    model: str = "flux-schnell"
    ratio: str = "square"
    steps: int = 25
    guidance: float = 7.5
    seed: int = -1
    style: str = ""


CFG = ProviderConfig()

MODELS = {
    "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "sd3": "stabilityai/stable-diffusion-3-medium-diffusers",
    "realvis": "SG161222/RealVisXL_V4.0",
}

RATIO_MAP = {
    "square": (1024, 1024),
    "portrait": (768, 1024),
    "landscape": (1024, 768),
    "wide": (1280, 720),
    "tall": (720, 1280),
}

DEFAULT_NEG = "blurry, low quality, distorted, watermark"


class ProviderError(Exception):
    pass


def _resolve_seed(seed: int) -> int:
    return random.randint(0, 99999) if seed == -1 else seed


def _to_data_uri(content: bytes, mime: str) -> str:
    return f"data:image/{mime};base64,{base64.b64encode(content).decode()}"


class HuggingFaceProvider:
    name = "Hugging Face"

    @staticmethod
    def generate(p: GenerationParams, width: int, height: int) -> str:
        if not CFG.hf_key:
            raise ProviderError("HF_API_KEY not set")

        model_id = MODELS.get(p.model, MODELS["flux-schnell"])
        url = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {CFG.hf_key}"}
        payload = {
            "inputs": p.prompt,
            "parameters": {
                "negative_prompt": p.negative or DEFAULT_NEG,
                "width": width,
                "height": height,
                "num_inference_steps": p.steps,
                "guidance_scale": p.guidance,
                "seed": _resolve_seed(p.seed),
            },
        }

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
        except requests.RequestException as exc:
            raise ProviderError(str(exc)) from exc

        if resp.status_code == 503:
            raise ProviderError("model loading, retry in 20s")
        if resp.status_code != 200:
            raise ProviderError(f"status {resp.status_code}: {resp.text[:200]}")

        return _to_data_uri(resp.content, "jpeg")


class StableHordeProvider:
    name = "Stable Horde"
    BASE = "https://stablehorde.net/api/v2"

    @staticmethod
    def _submit(p: GenerationParams, width: int, height: int) -> str:
        headers = {"apikey": CFG.horde_key, "Content-Type": "application/json"}
        payload = {
            "prompt": p.prompt + ("###" + p.negative if p.negative else ""),
            "params": {
                "width": width,
                "height": height,
                "steps": min(p.steps, 30),
                "cfg_scale": p.guidance,
                "seed": str(_resolve_seed(p.seed)),
                "n": 1,
            },
            "models": ["SDXL 1.0"],
            "r2": False,
        }
        resp = requests.post(
            f"{StableHordeProvider.BASE}/generate/async",
            headers=headers,
            json=payload,
            timeout=30,
        )
        if resp.status_code != 202:
            raise ProviderError(f"submit error {resp.status_code}")
        return resp.json()["id"]

    @staticmethod
    def _poll(job_id: str, headers: dict) -> dict:
        for _ in range(60):
            time.sleep(4)
            check = requests.get(
                f"{StableHordeProvider.BASE}/generate/check/{job_id}",
                headers=headers,
                timeout=10,
            ).json()
            if check.get("done"):
                return requests.get(
                    f"{StableHordeProvider.BASE}/generate/status/{job_id}",
                    headers=headers,
                    timeout=10,
                ).json()
        raise ProviderError("polling timeout")

    @staticmethod
    def generate(p: GenerationParams, width: int, height: int) -> str:
        headers = {"apikey": CFG.horde_key, "Content-Type": "application/json"}
        job_id = StableHordeProvider._submit(p, width, height)
        result = StableHordeProvider._poll(job_id, headers)
        img_url = result["generations"][0]["img"]
        img_bytes = requests.get(img_url, timeout=30).content
        return _to_data_uri(img_bytes, "webp")


class PollinationsProvider:
    name = "Pollinations"

    @staticmethod
    def generate(p: GenerationParams, width: int, height: int) -> str:
        seed = _resolve_seed(p.seed)
        url = (
            f"https://image.pollinations.ai/prompt/{quote(p.prompt)}"
            f"?width={width}&height={height}&seed={seed}"
            f"&nologo=true&enhance=true&model=flux"
        )
        resp = requests.get(url, timeout=90)
        if resp.status_code != 200:
            raise ProviderError("request failed")
        return _to_data_uri(resp.content, "jpeg")


PROVIDERS = (HuggingFaceProvider, StableHordeProvider, PollinationsProvider)


def _parse_params(data: dict) -> GenerationParams:
    return GenerationParams(
        prompt=(data.get("prompt") or "").strip(),
        negative=(data.get("negative") or "").strip(),
        model=data.get("model", "flux-schnell"),
        ratio=data.get("ratio", "square"),
        steps=int(data.get("steps", 25)),
        guidance=float(data.get("guidance", 7.5)),
        seed=int(data.get("seed", -1)),
        style=(data.get("style") or "").strip(),
    )


def _apply_style(p: GenerationParams) -> GenerationParams:
    if not p.style:
        return p
    return GenerationParams(
        prompt=f"{p.prompt}, {p.style} style",
        negative=p.negative,
        model=p.model,
        ratio=p.ratio,
        steps=p.steps,
        guidance=p.guidance,
        seed=p.seed,
        style=p.style,
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    params = _parse_params(data)

    if not params.prompt:
        return jsonify({"error": "Prompt required"}), 400

    params = _apply_style(params)
    width, height = RATIO_MAP.get(params.ratio, (1024, 1024))

    errors = []
    for provider in PROVIDERS:
        try:
            image = provider.generate(params, width, height)
            return jsonify({
                "image": image,
                "provider": provider.name,
                "model": params.model,
            })
        except Exception as exc:
            errors.append(f"{provider.name}: {exc}")

    return jsonify({"error": "All providers failed", "details": errors}), 500


@app.route("/models")
def list_models():
    return jsonify(list(MODELS.keys()))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
