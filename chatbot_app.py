import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# --- Load Environment ---
load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()

# --- Page Setup ---
st.set_page_config(
    page_title="WaterProofFish AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS for Modern UI ---
st.markdown("""
<style>
/* App background and text */
.stApp { background-color: #121212; color: #E0E0E0; font-family: 'Arial', sans-serif; }

/* Chat container styling */
.stChatMessage { border-radius: 20px; padding: 1rem 1.5rem; margin-bottom: 1rem; max-width: 70%; }

/* User message styling */
[data-testid="chat-message-container"]:has([data-testid="chat-avatar-user"]) {
    background-color: #004d99; /* Neon blue accent */
    border-color: #0078D4;
    margin-left: auto;
    margin-right: 0;
    color: #FFFFFF;
}

/* Bot message styling */
[data-testid="chat-message-container"]:has([data-testid="chat-avatar-bot"]) {
    background-color: #2A2A2A; /* Soft gray panel */
    border-color: #444444;
    margin-left: 0;
    margin-right: auto;
    color: #E0E0E0;
}

/* Chat timestamps */
.timestamp { font-size: 0.7rem; color: #AAAAAA; margin-left: 0.5rem; }

/* Page title */
h1 { color: #FFFFFF; text-align: center; padding-bottom: 1rem; }

/* Sidebar styling */
.css-1d391kg { background-color: #1E1E1E; padding: 1rem; }

/* Input box and button */
.stTextInput>div>div>input, .stButton>button {
    background-color: #2A2A2A;
    color: #FFFFFF;
    border-radius: 10px;
    border: 1px solid #0078D4;
    padding: 0.5rem 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- Initialize Chat Model ---
def initialize_chat(personality_instruction):
    try:
        model = genai.GenerativeModel('models/gemini-2.5-pro')
        chat = model.start_chat(history=[
            {'role': 'user', 'parts': [personality_instruction]},
            {'role': 'model', 'parts': ["Understood. I will follow the selected personality."]}
        ])
        return chat
    except Exception as e:
        st.error(f"Failed to initialize the chat model: {e}")
        st.stop()

# --- Sidebar Controls ---
with st.sidebar:
    st.header("Settings")
    
    # Personality selector
    personality = st.selectbox(
        "Select Chatbot Personality",
        ["Friendly", "Professional", "Casual"]
    )
    
    personality_map = {
        "Friendly": "Respond in a friendly and approachable manner.",
        "Professional": "Respond briefly and clearly, be professional and concise.",
        "Casual": "Respond in a casual, informal, friendly way."
    }
    personality_instruction = personality_map[personality]
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat = initialize_chat(personality_instruction)
        st.session_state.messages = []
        st.rerun()

# --- Initialize Session State ---
if 'chat' not in st.session_state:
    st.session_state.chat = initialize_chat(personality_instruction)
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?", "time": datetime.now()}]

# --- Main UI ---
st.title("🤖 WaterProofFish Chatbot")

# Display chat messages
for message in st.session_state.messages:
    timestamp = message.get("time", datetime.now()).strftime("%H:%M")
    with st.chat_message(message["role"]):
        st.markdown(f"{message['content']}<span class='timestamp'>{timestamp}</span>", unsafe_allow_html=True)

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt, "time": datetime.now()})
    with st.chat_message("user"):
        st.markdown(f"{prompt}<span class='timestamp'>{datetime.now().strftime('%H:%M')}</span>", unsafe_allow_html=True)
    
    # Generate bot response
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.chat.send_message(f"{personality_instruction}\nUser: {prompt}")
            response_text = response.text
            st.session_state.messages.append({"role": "assistant", "content": response_text, "time": datetime.now()})
            with st.chat_message("assistant"):
                st.markdown(f"{response_text}<span class='timestamp'>{datetime.now().strftime('%H:%M')}</span>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while getting the response: {e}")
