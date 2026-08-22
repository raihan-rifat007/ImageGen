from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

AGNES_API_KEY = os.getenv('AGNES_API_KEY')
AGNES_API_URL = 'https://apihub.agnes-ai.com/v1/images/generations'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        style = data.get('style', '')
        ratio = data.get('ratio', '1:1')
        size = data.get('size', '2K')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        if not AGNES_API_KEY:
            return jsonify({'error': 'AGNES_API_KEY not configured'}), 500

        full_prompt = f"{prompt}, {style}" if style else prompt

        payload = {
            'model': 'agnes-image-2.1-flash',
            'prompt': full_prompt,
            'size': size,
            'ratio': ratio,
            'extra_body': {
                'response_format': 'url'
            }
        }

        headers = {
            'Authorization': f'Bearer {AGNES_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post(AGNES_API_URL, json=payload, headers=headers, timeout=60)

        if response.status_code != 200:
            return jsonify({'error': f'API error: {response.status_code}'}), response.status_code

        result = response.json()

        if result.get('data') and len(result['data']) > 0:
            image_url = result['data'][0].get('url')
            if not image_url and result['data'][0].get('b64_json'):
                image_url = f"data:image/png;base64,{result['data'][0]['b64_json']}"

            if image_url:
                return jsonify({'image': image_url})

        return jsonify({'error': 'No image generated'}), 500

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout. Please try again.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
