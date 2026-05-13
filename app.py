import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURATION ---
# Secrets mein GEMINI_API_KEY hona zaroori hai
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_KEY)

@app.route('/')
def home():
    # Royal UI for Dilansh Jain
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>JARVIS OMNI-ENGINE V64</title>
        <style>
            body { background: #000; color: #00d4ff; font-family: 'Segoe UI', sans-serif; text-align: center; margin: 0; }
            .container { border: 2px solid #00d4ff; border-radius: 20px; padding: 30px; width: 85%; margin: 5% auto; background: rgba(0,0,0,0.9); box-shadow: 0 0 40px #00d4ff33; }
            input { width: 90%; padding: 15px; background: transparent; border: 1px solid #00d4ff; color: white; border-radius: 10px; margin-bottom: 20px; font-size: 1.1em; outline: none; }
            .btn { padding: 15px 40px; background: #00d4ff; color: black; border: none; border-radius: 50px; font-weight: bold; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; }
            .btn:hover { background: white; box-shadow: 0 0 20px #00d4ff; }
            #output { margin-top: 20px; padding: 25px; border: 1px solid #222; min-height: 100px; text-align: left; background: rgba(255,255,255,0.05); border-radius: 15px; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🤖 JARVIS OMNI-ENGINE</h2>
            <div id="output">System Initialized. Awaiting your command, Sir.</div>
            <br>
            <input type="text" id="userInput" placeholder="What is your command, Sir?">
            <br>
            <button class="btn" onclick="sendMessage()">Brain Link</button>
        </div>

        <script>
            async function sendMessage() {
                const input = document.getElementById('userInput');
                const output = document.getElementById('output');
                const msg = input.value;
                if(!msg) return;

                output.innerText = "Jarvis is processing...";
                try {
                    const response = await fetch('/chat?msg=' + encodeURIComponent(msg));
                    const data = await response.json();
                    output.innerText = data.response;
                    input.value = "";
                } catch (e) {
                    output.innerText = "Sir, the neural connection was interrupted.";
                }
            }
        </script>
    </body>
    </html>
    """

@app.route('/chat')
def chat():
    user_msg = request.args.get('msg')
    try:
        # --- FIXED MODEL NAME FOR V1BETA ---
        # "models/" prefix lagane se 404 error solve ho jata hai
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # System instructions with your identity
        response = model.generate_content(f"You are JARVIS. Owner: Dilansh. Reply to: {user_msg}")
        return jsonify({"response": response.text})
    except Exception as e:
        # Detailed error log for debugging
        return jsonify({"response": f"Sir, error in core: {str(e)}"})

if __name__ == '__main__':
    # Replit expected port is 5000 based on your latest logs
    app.run(host='0.0.0.0', port=5000)
