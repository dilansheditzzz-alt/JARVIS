import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import requests
import base64

app = Flask(__name__)

# --- API CONFIG ---
# Ye keys hum Replit ke 'Secrets' mein daalenge
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
STABILITY_KEY = os.environ.get('STABILITY_API_KEY')

genai.configure(api_key=GEMINI_KEY)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>JARVIS V64 PRO</title>
        <style>
            body { background: radial-gradient(circle, #021B79, #000); color: #00d4ff; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 50px; }
            .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(0, 212, 255, 0.2); padding: 40px; width: 70%; margin: auto; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8); }
            input { width: 80%; padding: 15px; border-radius: 10px; border: 1px solid #00d4ff; background: rgba(0,0,0,0.5); color: white; margin-bottom: 20px; outline: none; }
            .btn { padding: 15px 30px; border-radius: 50px; border: none; background: #00d4ff; color: #021B79; font-weight: bold; cursor: pointer; transition: 0.3s; margin: 10px; text-transform: uppercase; }
            .btn:hover { box-shadow: 0 0 20px #00d4ff; transform: scale(1.05); }
            #status { color: #64ffda; font-weight: lighter; margin-bottom: 20px; }
            #response { background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; min-height: 50px; line-height: 1.6; }
            img { border-radius: 15px; margin-top: 20px; border: 2px solid #00d4ff; max-width: 100%; }
        </style>
    </head>
    <body>
        <div class="glass-card">
            <h1>🤖 JARVIS V64 PRO</h1>
            <div id="status">Neural Link: Connected</div>
            <input type="text" id="command" placeholder="Enter command for Jarvis, Sir Dilansh...">
            <br>
            <button class="btn" onclick="askJarvis()">Analyze</button>
            <button class="btn" onclick="generateArt()">Synthesize Art</button>
            <div id="response">Waiting for command...</div>
            <div id="art-box"></div>
        </div>

        <script>
            async function askJarvis() {
                const cmd = document.getElementById('command').value;
                document.getElementById('response').innerText = "Thinking...";
                const res = await fetch('/chat?msg=' + encodeURIComponent(cmd));
                const data = await res.json();
                document.getElementById('response').innerText = data.response;
            }
            async function generateArt() {
                const cmd = document.getElementById('command').value;
                document.getElementById('response').innerText = "Generating Art...";
                const res = await fetch('/art?msg=' + encodeURIComponent(cmd));
                const data = await res.json();
                if(data.image) {
                    document.getElementById('art-box').innerHTML = `<img src="data:image/png;base64,${data.image}">`;
                    document.getElementById('response').innerText = "Art successfully synthesized.";
                } else {
                    document.getElementById('response').innerText = "Error in Art Engine.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Respond as Jarvis to Dilansh: {msg}")
    return jsonify({"response": response.text})

@app.route('/art')
def art():
    msg = request.args.get('msg')
    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
    headers = {"Authorization": f"Bearer {STABILITY_KEY}"}
    body = {"text_prompts": [{"text": msg}], "cfg_scale": 7, "height": 512, "width": 512, "samples": 1}
    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 200:
        return jsonify({"image": res.json()["artifacts"][0]["base64"]})
    return jsonify({"error": "Art engine failed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
