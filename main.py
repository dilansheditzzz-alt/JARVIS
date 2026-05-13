import os
import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="JARVIS OMNI-ENGINE", page_icon="🤖", layout="centered")

# --- UI STYLE (Royal Cyan & Black) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00d4ff; }
    .stTextInput > div > div > input { background-color: #111; color: #00d4ff; border: 1px solid #00d4ff; border-radius: 10px; }
    .stButton > button { background-color: #00d4ff; color: black; border-radius: 50px; width: 100%; font-weight: bold; border: none; }
    .stButton > button:hover { background-color: white; color: black; box-shadow: 0 0 20px #00d4ff; }
    .chat-box { border: 1px solid #222; padding: 20px; border-radius: 15px; background: rgba(0, 212, 255, 0.05); }
    </style>
    """, unsafe_allow_index=True)

# --- API CONFIG ---
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_KEY)

# --- MODEL INITIALIZATION (FIXED) ---
# Direct access to the stable version to avoid 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>🤖 JARVIS OMNI-ENGINE</h1>", unsafe_allow_index=True)
st.markdown("<p style='text-align: center; color: #666;'>USER: DILANSH JAIN | STATUS: NEURAL LINK ACTIVE</p>", unsafe_allow_index=True)

# --- CHAT LOGIC ---
if 'history' not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Command me, Sir...", key="input")

if st.button("BRAIN LINK"):
    if user_input:
        try:
            # JARVIS Personality Layer
            prompt = f"Role: You are JARVIS, the loyal and smart AI for Dilansh Jain. Mood: Royal. Context: Tonk, Rajasthan. Task: {user_input}"
            response = model.generate_content(prompt)
            
            # Save to history
            st.session_state.history.append({"user": user_input, "jarvis": response.text})
        except Exception as e:
            st.error(f"Sir, connection failed: {str(e)}")

# --- DISPLAY CHAT ---
st.markdown("---")
for chat in reversed(st.session_state.history):
    st.markdown(f"<div class='chat-box'><b>You:</b> {chat['user']}<br><br><b style='color: #00d4ff;'>Jarvis:</b> {chat['jarvis']}</div>", unsafe_allow_index=True)
    st.markdown("<br>", unsafe_allow_index=True)
