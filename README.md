```markdown
# AI Image Generator Web Application

A full-stack AI image generation app built with Flask and Pollinations.ai.  
Users describe a scene in text and receive an AI-generated image, with support for multiple art styles, image history, and dark mode.

## Features

- Text prompt input with real‑time AI generation
- Multiple art styles (Realistic, Anime, Oil Painting, etc.)
- Aspect ratio selection (Square, Portrait, Landscape)
- "Surprise me" random prompt generator
- Regenerate button for new results with the same prompt
- History saved in browser localStorage (Contact Sheet)
- Full gallery view in a modal
- Dark mode toggle (preference saved)
- One‑click download of generated images
- Toast notifications for actions

## Tech Stack

- Backend: Python, Flask
- Image Generation: Pollinations.ai (free, no API key)
- Frontend: HTML, CSS, Vanilla JS
- Storage: Browser localStorage
- Fonts: Fraunces + Inter (Google Fonts)

## Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/tubashakeel67-ai/ai-image-generator.git
   cd ai-image-generator
```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open in browser:
   ```
   http://127.0.0.1:5000
   ```

Deploy to Render (Free)

1. Push this repository to GitHub.
2. Create a free account on Render.
3. Click New + → Web Service.
4. Connect your GitHub repository.
5. Configure:
   · Environment: Python 3
   · Build Command: pip install -r requirements.txt
   · Start Command: gunicorn app:app
6. Click Create Web Service.
7. Your app will be live at https://your-app-name.onrender.com.

The free tier spins down after inactivity – the first visit may take ~60s to wake up.

Project Structure

```
ai-image-generator/
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

Future Improvements

· User authentication for cross‑device history
· Server‑side image history with a database
· Batch image generation

Author

Tuba Shakeel
GitHub: tubashakeel67-ai
LinkedIn: Tuba Shakeel

```

---

## 🚀 Quick Deployment Steps (Summary)

1. Create all the above files in your local project folder.
2. Initialize Git and push to a GitHub repository.
3. Go to [Render](https://render.com), sign up, and create a new Web Service.
4. Connect your repo, use the settings as described in the README.
5. Deploy – your app will be online in a few minutes.

You can also use **PythonAnywhere** or **Heroku** (paid) with similar steps, but Render is the easiest free option.

Let me know if you need any adjustments!
