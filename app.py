import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIG ---
# Make sure GEMINI_API_KEY is in your Secrets
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDB5QbDVJSrurd0G7lXUHRZVpRPqxSdv8c')
genai.configure(api_key=GEMINI_KEY)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>JARVIS OMNI-ENGINE</title>
        <style>
            body { background: #000; color: #00d4ff; font-family: 'Segoe UI', sans-serif; text-align: center; }
            .terminal { border: 2px solid #00d4ff; border-radius: 20px; padding: 30px; width: 85%; margin: 5% auto; background: rgba(0,0,0,0.9); box-shadow: 0 0 30px #00d4ff55; }
            input { width: 90%; padding: 15px; background: transparent; border: 1px solid cyan; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 1.1em; }
            .btn { padding: 15px 35px; background: #00d4ff; color: black; border: none; border-radius: 50px; font-weight: bold; cursor: pointer; text-transform: uppercase; }
            #output { margin-top: 20px; padding: 25px; border: 1px solid #111; min-height: 80px; text-align: left; background: rgba(255,255,255,0.05); border-radius: 15px; }
        </style>
    </head>
    <body>
        <div class="terminal">
            <h2>🤖 JARVIS OMNI-ENGINE V64</h2>
            <p>User: Dilansh Jain | Status: Online</p>
            <div id="output">Neural Link Ready. System Awaiting Command...</div>
            <br>
            <input type="text" id="in" placeholder="Command me, Sir...">
            <br>
            <button class="btn" onclick="run()">BRAIN LINK</button>
        </div>
        <script>
            async function run() {
                const msg = document.getElementById('in').value;
                const out = document.getElementById('output');
                out.innerText = "Jarvis is thinking...";
                try {
                    // Port 5000 compatibility check
                    const response = await fetch('/chat?msg=' + encodeURIComponent(msg));
                    const data = await response.json();
                    out.innerText = data.response;
                } catch(e) {
                    out.innerText = "Error: Neural connection timed out. Please refresh.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    try:
        # Final model check to avoid 404
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = f"Role: Jarvis. Owner: Dilansh Jain. Mood: Loyal & Smart. Task: {msg}"
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Sir, I encountered a core error: {str(e)}"})

if __name__ == '__main__':
    # Replit Agent uses port 5000
    app.run(host='0.0.0.0', port=5000)
