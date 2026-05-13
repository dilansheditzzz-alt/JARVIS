import os
import base64
import requests
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# --- 1. CORE ENGINE CONFIG (AI BRAIN) ---
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDB5QbDVJSrurd0G7lXUHRZVpRPqxSdv8c')
STABILITY_KEY = os.environ.get('STABILITY_API_KEY', 'sk-dBrp8z3MiVb03Qt5NooKENix0ljoo1I8fC0tgMPBZiU2MjYh')

genai.configure(api_key=GEMINI_KEY)

# Short-term Memory (Context Understanding)
chat_history = []

# --- 2. JARVIS MODES & INTELLIGENCE ---
def get_jarvis_response(user_input, image_data=None):
    # Model Fix: models/ prefix added to solve 404 error
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    # Context/Memory Management
    context = f"System: Jarvis. Owner: Dilansh Jain. Location: Tonk. History: {chat_history[-5:]}\n"
    full_prompt = f"{context} User: {user_input}"
    
    if image_data:
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        response = model.generate_content([full_prompt, img])
    else:
        response = model.generate_content(full_prompt)
    
    chat_history.append({"user": user_input, "jarvis": response.text})
    return response.text

# --- 3. WEB INTERFACE (ROYAL GLASSMORPHISM) ---
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>JARVIS V64 OMNI-ENGINE</title>
        <style>
            body { background: radial-gradient(circle, #001f3f, #000); color: #00d4ff; font-family: 'Orbitron', sans-serif; margin: 0; padding: 20px; }
            .jarvis-ui { border: 2px solid #00d4ff; border-radius: 30px; padding: 20px; background: rgba(0,0,0,0.8); box-shadow: 0 0 50px rgba(0, 212, 255, 0.2); max-width: 900px; margin: auto; }
            .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 20px; }
            .status-bar { border-bottom: 1px solid #00d4ff; padding: 10px; display: flex; justify-content: space-between; font-size: 12px; }
            textarea { width: 95%; background: transparent; border: 1px solid #00d4ff; color: white; border-radius: 10px; padding: 15px; margin-top: 20px; }
            .btn { background: #00d4ff; color: black; border: none; padding: 15px; border-radius: 50px; font-weight: bold; cursor: pointer; transition: 0.5s; width: 100%; margin-top: 10px; }
            .btn:hover { box-shadow: 0 0 20px white; background: white; }
            #output { border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin-top: 20px; min-height: 100px; background: rgba(255,255,255,0.05); text-align: left; }
            img { width: 100%; border-radius: 15px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="jarvis-ui">
            <div class="status-bar">
                <span>SYSTEM: V64.0.1 ALPHA</span>
                <span>CORE: GEMINI-PRO-FLASH</span>
                <span>STATUS: NEURAL LINK ACTIVE</span>
            </div>
            <h1>🤖 JARVIS OMNI-ENGINE</h1>
            <div id="output">Welcome back, Sir Dilansh. All systems are nominal. Ready for command...</div>
            <div id="art-display"></div>
            
            <textarea id="cmd" placeholder="Speak or Type: 'Scan this image', 'Generate a royal car', 'Control lights'..."></textarea>
            
            <div class="feature-grid">
                <button class="btn" onclick="execute('chat')">🧠 BRAIN LINK</button>
                <button class="btn" onclick="execute('art')">🎨 ART SYNTH</button>
                <button class="btn" onclick="execute('vision')">👁️ VISION SCAN</button>
            </div>
        </div>

        <script>
            async function execute(mode) {
                const cmd = document.getElementById('cmd').value;
                const out = document.getElementById('output');
                out.innerText = "Processing through Neural Layers...";
                
                let endpoint = mode === 'chat' ? '/chat' : '/art';
                const res = await fetch(`${endpoint}?msg=${encodeURIComponent(cmd)}`);
                const data = await res.json();
                
                if(data.response) out.innerText = data.response;
                if(data.image) {
                    document.getElementById('art-display').innerHTML = `<img src="data:image/png;base64,${data.image}">`;
                    out.innerText = "Visualization complete, Sir.";
                }
            }
        </script>
    </body>
    </html>
    """

# --- 4. API ROUTES (THE CORE) ---
@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    response = get_jarvis_response(msg)
    return jsonify({"response": response})

@app.route('/art')
def art():
    msg = request.args.get('msg')
    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
    headers = {"Authorization": f"Bearer {STABILITY_KEY}"}
    body = {"text_prompts": [{"text": msg}], "cfg_scale": 7, "height": 512, "width": 512, "samples": 1}
    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 200:
        return jsonify({"image": res.json()["artifacts"][0]["base64"]})
    return jsonify({"error": "Failed"}), 400

if __name__ == '__main__':
    # Forcefully use port 5000 for Replit Agent compatibility
    app.run(host='0.0.0.0', port=5000)
