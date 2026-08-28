import os, requests, base64, time, random
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY", "")
HORDE_APIKEY = os.getenv("HORDE_APIKEY", "0000000000")

MODELS = {
    "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    "flux-dev": "black-forest-labs/FLUX.1-dev",
    "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
    "sd3": "stabilityai/stable-diffusion-3-medium-diffusers",
    "realvis": "SG161222/RealVisXL_V4.0",
    "playground": "playgroundai/playground-v2.5-1024px-aesthetic",
}

RATIO_MAP = {
    "square": (1024, 1024),
    "portrait": (768, 1024),
    "landscape": (1024, 768),
    "wide": (1280, 720),
    "tall": (720, 1280),
    "ultrawide": (1536, 640),
}

def generate_hf(prompt, neg, model_id, width, height, steps, guidance, seed):
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": neg or "blurry, low quality, distorted, watermark",
            "width": width,
            "height": height,
            "num_inference_steps": int(steps),
            "guidance_scale": float(guidance),
            "seed": int(seed) if int(seed) != -1 else random.randint(0, 99999),
        }
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code == 503:
        raise Exception("HF model loading, retry in 20s")
    if resp.status_code != 200:
        raise Exception(f"HF error {resp.status_code}: {resp.text[:200]}")
    b64 = base64.b64encode(resp.content).decode()
    return f"data:image/jpeg;base64,{b64}"

def generate_horde(prompt, neg, width, height, steps, guidance, seed):
    headers = {"apikey": HORDE_APIKEY, "Content-Type": "application/json"}
    payload = {
        "prompt": prompt + ("###" + neg if neg else ""),
        "params": {
            "width": width,
            "height": height,
            "steps": min(int(steps), 30),
            "cfg_scale": float(guidance),
            "seed": str(seed) if int(seed) != -1 else str(random.randint(0, 99999)),
            "n": 1,
        },
        "models": ["SDXL 1.0"],
        "r2": False,
    }
    r = requests.post("https://stablehorde.net/api/v2/generate/async", headers=headers, json=payload, timeout=30)
    if r.status_code != 202:
        raise Exception(f"Horde submit error: {r.status_code}")
    job_id = r.json()["id"]
    for _ in range(60):
        time.sleep(4)
        check = requests.get(f"https://stablehorde.net/api/v2/generate/check/{job_id}", headers=headers, timeout=10).json()
        if check.get("done"):
            result = requests.get(f"https://stablehorde.net/api/v2/generate/status/{job_id}", headers=headers, timeout=10).json()
            img_url = result["generations"][0]["img"]
            img_b64 = base64.b64encode(requests.get(img_url, timeout=30).content).decode()
            return f"data:image/webp;base64,{img_b64}"
    raise Exception("Horde timeout")

def generate_pollinations(prompt, width, height, seed):
    from urllib.parse import quote
    s = seed if int(seed) != -1 else random.randint(0, 99999)
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}?width={width}&height={height}&seed={s}&nologo=true&enhance=true&model=flux"
    resp = requests.get(url, timeout=90)
    if resp.status_code != 200:
        raise Exception("Pollinations failed")
    b64 = base64.b64encode(resp.content).decode()
    return f"data:image/jpeg;base64,{b64}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = (data.get("prompt") or "").strip()
    neg = (data.get("negative") or "").strip()
    model_k = data.get("model", "flux-schnell")
    ratio = data.get("ratio", "square")
    steps = data.get("steps", 28)
    guidance = data.get("guidance", 7.5)
    seed = data.get("seed", -1)
    style = data.get("style", "")
    
    if not prompt:
        return jsonify({"error": "Prompt required"}), 400
    
    if style:
        prompt = f"{prompt}, {style} style"
    
    w, h = RATIO_MAP.get(ratio, (1024, 1024))
    err_log = []
    
    if HF_API_KEY:
        model_id = MODELS.get(model_k, MODELS["flux-schnell"])
        try:
            img = generate_hf(prompt, neg, model_id, w, h, steps, guidance, seed)
            return jsonify({"image": img, "provider": "Hugging Face", "model": model_k})
        except Exception as e:
            err_log.append(f"HF: {e}")
    
    try:
        img = generate_horde(prompt, neg, w, h, steps, guidance, seed)
        return jsonify({"image": img, "provider": "Stable Horde", "model": "SDXL"})
    except Exception as e:
        err_log.append(f"Horde: {e}")
    
    try:
        img = generate_pollinations(prompt, w, h, seed)
        return jsonify({"image": img, "provider": "Pollinations", "model": "Flux"})
    except Exception as e:
        err_log.append(f"Pollinations: {e}")
    
    return jsonify({"error": "All providers failed", "details": err_log}), 500

@app.route("/models")
def list_models():
    return jsonify(list(MODELS.keys()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
