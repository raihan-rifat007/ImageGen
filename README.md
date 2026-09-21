<div align="center">

# 🎨 AI Image Studio

**A production-grade AI image generation platform powered by multiple free providers**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)]()

**Generate stunning AI images with zero cost — powered by Hugging Face, Stable Horde & Pollinations**

[Features](#-features) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Architecture](#-architecture) · [Deployment](#-deployment)

</div>

---

## 📖 Overview

**AI Image Studio** is a modern, self-hosted AI image generation platform that unifies multiple free AI providers into a single, elegant API. Built with Flask and a premium web UI, it delivers production-grade performance without requiring paid API keys.

### Why AI Image Studio?

- 🆓 **Zero Cost** — Uses free AI providers with automatic fallback
- 🎨 **Premium UI** — Modern glassmorphic design with dark/light themes
- ⚡ **Multi-Provider** — Automatic failover across 3 providers
- 🎯 **6 AI Models** — Flux, SDXL, Turbo, Realism & more
- 🖼️ **Flexible Ratios** — 6 aspect ratios from square to ultrawide
- 🔧 **Advanced Controls** — Steps, guidance, seed, batch generation
- 💾 **Local Storage** — Prompt library, history & favorites
- ⌨️ **Keyboard First** — Command palette & shortcuts
- 📱 **Fully Responsive** — Desktop, tablet & mobile
- 🚀 **Production Ready** — Deployed on any Python host

---

## ✨ Features

### Core Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| **Multi-Provider Fallback** | Hugging Face → Stable Horde → Pollinations | ✅ |
| **6 AI Models** | Flux, Turbo, SDXL, Realism, Dev, SD3 | ✅ |
| **6 Aspect Ratios** | 1:1, 3:4, 4:3, 16:9, 9:16, 21:9 | ✅ |
| **16 Art Styles** | Photorealistic, Anime, Cinematic & more | ✅ |
| **Batch Generation** | Generate 1, 2, 4, or 8 images at once | ✅ |
| **Advanced Controls** | Steps, guidance scale, custom seed | ✅ |
| **Prompt Library** | Save & reuse favorite prompts | ✅ |
| **Generation History** | Track recent generations | ✅ |
| **Favorites System** | Star your best images | ✅ |
| **Batch Selection** | Multi-select for bulk actions | ✅ |
| **Layout Modes** | Compact, Default, Large grid | ✅ |
| **Search & Filter** | Filter gallery by prompt/model | ✅ |
| **Keyboard Shortcuts** | Full shortcut support | ✅ |
| **Dark/Light Theme** | Auto-detect + manual toggle | ✅ |

### UI Highlights

- 🎭 **Glassmorphic Design** — Frosted glass aesthetic
- 🌈 **Violet-Fuchsia Gradient** — Modern color palette
- ✨ **Micro-animations** — Smooth 60fps transitions
- 🖼️ **Lightbox Viewer** — Full-screen image preview with zoom
- 🎛️ **Command Palette** — Raycast-style ⌘K menu
- 📊 **Live Status** — Real-time API status indicator
- 🔔 **Toast Notifications** — Elegant feedback system

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **pip** package manager
- **Modern browser** (Chrome, Firefox, Safari, Edge)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/raihan07/ai-image-studio.git
cd ai-image-studio

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install flask requests

# 5. (Optional) Set Hugging Face API key
export HF_API_KEY="hf_your_key_here"
# Windows: set HF_API_KEY=hf_your_key_here

# 6. Run the application
python app.py
```

Open your browser: http://localhost:5000

---

📁 Project Structure

```
ai-image-studio/
├── app.py                  # Flask application + providers
├── templates/
│   └── index.html         # Premium web UI
├── static/
│   └── assets/
│       └── Logo.png       # Brand logo
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

---

🔌 API Reference

Base URL

```
http://localhost:5000
```

Endpoints

1. Home Page

```http
GET /
```

Returns the main web interface.

---

2. Generate Image

```http
POST /generate
Content-Type: application/json
```

Request Body:

```json
{
  "prompt": "A serene mountain landscape at sunset",
  "negative": "blurry, low quality",
  "model": "flux",
  "ratio": "square",
  "steps": 30,
  "guidance": 7.5,
  "seed": -1,
  "style": "Cinematic"
}
```

Parameters:

Parameter Type Required Default Description
prompt string ✅ Yes — Image description
negative string ❌ No "" What to avoid
model string ❌ No flux Model ID
ratio string ❌ No square Aspect ratio
steps integer ❌ No 25 Sampling steps (10-50)
guidance float ❌ No 7.5 CFG scale (1-20)
seed integer ❌ No -1 Seed (-1 = random)
style string ❌ No "" Art style modifier

Response (Success):

```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "provider": "Hugging Face",
  "model": "flux"
}
```

Response (Error):

```json
{
  "error": "All providers failed",
  "details": [
    "Hugging Face: HF_API_KEY not set",
    "Stable Horde: polling timeout",
    "Pollinations: request failed"
  ]
}
```

Status Codes:

Code Meaning
200 Success
400 Missing/invalid prompt
500 All providers failed

---

3. List Models

```http
GET /models
```

Response:

```json
["sdxl", "flux-schnell", "flux-dev", "sd3", "realvis"]
```

---

🎨 Available Options

Models

ID Label Best For
flux Flux Photorealistic, fast
turbo Turbo Fastest generation
stable-diffusion-xl-base-1.0 SDXL High detail & art
flux-realism Flux Realism Ultra realistic
flux-schnell Flux Schnell Quick drafts
realvis RealVisXL Portraits

Aspect Ratios

Key Label Dimensions Best For
square 1:1 1024×1024 Social media
portrait 3:4 768×1024 Portraits
landscape 4:3 1024×768 Classic photos
wide 16:9 1280×720 Wallpapers
tall 9:16 720×1280 Stories/Reels
ultrawide 21:9 1536×640 Cinematic

Art Styles

Photorealistic · Cinematic · Oil Painting · Watercolor · Anime · Digital Art · Sketch · 3D Render · Fantasy · Pixel Art · Minimalist · Dark Fantasy · Neon Noir · Vintage · Studio Portrait · Isometric

---

🏗️ Architecture

System Design

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  HTML + CSS + Vanilla JS (Single Page)           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/JSON
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   Flask Application                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Routes: /, /generate, /models                    │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Provider Orchestrator (Automatic Failover)       │  │
│  └───────────────────────────────────────────────────┘  │
└─────┬─────────────────┬─────────────────┬───────────────┘
      │                 │                 │
      ▼                 ▼                 ▼
┌───────────┐    ┌───────────┐    ┌────────────────┐
│ Hugging   │    │ Stable    │    │ Pollinations   │
│ Face API  │    │ Horde     │    │ (Fallback)     │
└───────────┘    └───────────┘    └────────────────┘
```

Code Architecture

Object-Oriented Design:

```python
@dataclass(frozen=True)
class GenerationParams:
    prompt: str
    negative: str
    model: str
    ratio: str
    steps: int
    guidance: float
    seed: int
    style: str

class HuggingFaceProvider:
    name = "Hugging Face"
    @staticmethod
    def generate(p: GenerationParams, w: int, h: int) -> str:
        ...

class StableHordeProvider:
    name = "Stable Horde"
    ...

class PollinationsProvider:
    name = "Pollinations"
    ...
```

Provider Fallback Chain

```
1. Hugging Face (if API key set)
   ↓ failed?
2. Stable Horde (community GPUs)
   ↓ failed?
3. Pollinations (public API)
   ↓ failed?
Return error with all details
```

Design Patterns Used

· Dataclass — Type-safe data containers
· Strategy Pattern — Interchangeable providers
· Static Factory — Provider generation methods
· Custom Exceptions — Clean error handling
· Immutable Config — Frozen dataclass

---

🚢 Deployment

Option 1: Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variable (optional)
vercel env add HF_API_KEY
```

Option 2: Render

1. Push code to GitHub
2. Create New Web Service on Render
3. Connect repository
4. Configure:
   · Build: pip install -r requirements.txt
   · Start: gunicorn app:app
5. Add environment variables
6. Deploy

Option 3: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login & deploy
railway login
railway init
railway up
```

Option 4: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
```

```bash
docker build -t ai-image-studio .
docker run -p 5000:5000 -e HF_API_KEY=hf_xxx ai-image-studio
```

Option 5: Manual VPS

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

---

⚙️ Configuration

Environment Variables

Variable Required Default Description
HF_API_KEY ❌ No "" Hugging Face token
HORDE_APIKEY ❌ No 0000000000 Stable Horde key
PORT ❌ No 5000 Server port

Getting API Keys

Hugging Face (Optional)

1. Visit huggingface.co/settings/tokens
2. Create new token with read access
3. Add to environment: HF_API_KEY=hf_xxxxx

Benefits: Faster generation, access to premium models

Stable Horde (Optional)

1. Register at stablehorde.net
2. Get API key from profile
3. Add: HORDE_APIKEY=your_key

Benefits: Higher priority queue, faster processing

---

⌨️ Keyboard Shortcuts

Shortcut Action
⌘K / Ctrl+K Open command palette
⌘↵ / Ctrl+Enter Generate image
⌘B / Ctrl+B Toggle sidebar
⌘L / Ctrl+L Open prompt library
⌘H / Ctrl+H Open history
⌘J / Ctrl+J Toggle theme
⌘⇧C / Ctrl+Shift+C Clear all images
/ Focus search
? Show shortcuts
Esc Close overlays

---

🧪 Testing

API Tests

```bash
# Test health
curl http://localhost:5000/models

# Test generation
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cyberpunk city at night",
    "model": "flux",
    "ratio": "wide",
    "steps": 30
  }'

# Test with style
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A portrait of a woman",
    "style": "Cinematic",
    "ratio": "portrait"
  }'
```

Python Client Example

```python
import requests

class AIImageStudio:
    def __init__(self, base_url="http://localhost:5000"):
        self.base = base_url.rstrip("/")
    
    def generate(self, prompt, **kwargs):
        payload = {"prompt": prompt, **kwargs}
        r = requests.post(f"{self.base}/generate", json=payload, timeout=120)
        r.raise_for_status()
        return r.json()
    
    def models(self):
        r = requests.get(f"{self.base}/models")
        return r.json()

# Usage
studio = AIImageStudio()
result = studio.generate(
    prompt="A majestic lion in the savanna",
    model="flux",
    ratio="wide",
    style="Photorealistic"
)
print(f"Generated via: {result['provider']}")
```

---

🎯 Use Cases

· Content Creation — Blog images, thumbnails, social posts
· Design Prototyping — Quick concept visualization
· Education — Teaching AI concepts
· Personal Projects — Wallpapers, art, gifts
· Bot Integration — Discord/Telegram/Messenger bots
· Research — Prompt engineering experiments

---

🔒 Security & Best Practices

· ✅ No user data stored on server
· ✅ All API keys from environment
· ✅ No logging of prompts
· ✅ CORS handled properly
· ✅ Input validation
· ✅ Graceful error handling

Recommendations

· 🔐 Never commit .env files
· 🔐 Use HTTPS in production
· 🔐 Rate limit public deployments
· 🔐 Add authentication for private use
· 🔐 Monitor provider usage limits

---

🐛 Troubleshooting

Common Issues

Issue Solution
HF model loading Wait 20s, first request cold-starts
Horde timeout High demand, try again later
Slow generation Reduce steps or use turbo model
No images Check browser console, verify prompt
Port in use Change port: app.run(port=5001)

Debug Mode

```python
if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

Logs

```bash
# Linux/macOS
tail -f /var/log/ai-studio.log

# Windows PowerShell
Get-Content ai-studio.log -Wait
```

---

📈 Performance

Metric Value
Cold start ~3s
Generation 5–30s
Concurrent users 10+
Memory usage ~150MB
Image size 100–500KB

Optimization Tips

· Use turbo model for speed
· Reduce steps to 20–25
· Use -1 seed for variety
· Enable Hugging Face for priority
· Cache prompts with library

---

🤝 Contributing

Contributions welcome! Please follow these steps:

```bash
# 1. Fork the repo
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Commit changes
git commit -m "Add amazing feature"

# 4. Push to branch
git push origin feature/amazing-feature

# 5. Open Pull Request
```

Development Guidelines

· Follow PEP 8 for Python
· Use type hints
· Write docstrings
· Test before submitting

---

📄 License

Licensed under the MIT License — see LICENSE for details.

---

🙏 Acknowledgments

· Hugging Face — Inference API infrastructure
· Stable Horde — Community GPU network
· Pollinations — Free fallback API
· Flask — Web framework
· Open Source Community — Libraries and tools

---

📞 Contact & Support

Channel Link
GitHub Issues Report Bug
Discussions Ask Questions
Creator @raihan07

---

<div align="center">

Built with ❤️ by raihan07

⭐ Star this project if you find it useful! ⭐

</div>
