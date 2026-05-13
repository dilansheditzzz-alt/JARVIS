import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURATION ---
# Make sure GEMINI_API_KEY is in your Replit Secrets
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_KEY)

@app.route('/')
def home():
    # Royal UI Design for Dilansh Jain
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
            .status { font-size: 0.8em; color: #666; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status">NEURAL LINK: ACTIVE | LOCATION: TONK | USER: DILANSH JAIN</div>
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
                    output.innerText = "Sir, the neural connection was interrupted. Please check the console.";
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
        # FIXED: Correct model path for Gemini 1.5 Flash
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        # Adding your requested features in System Prompt
        system_prompt = (
            "You are JARVIS, the highly advanced AI assistant of Dilansh Jain. "
            "Location: Tonk, Rajasthan. "
            "Personality: Royal, loyal, professional but with a sense of humor. "
            "Capabilities: Real-time thinking, deep reasoning, and adaptive intelligence. "
            f"Current task: {user_msg}"
        )
        
        response = model.generate_content(system_prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Sir, I encountered a core error: {str(e)}"})

if __name__ == '__main__':
    # Replit Agent Port Compatibility
    app.run(host='0.0.0.0', port=5000)
