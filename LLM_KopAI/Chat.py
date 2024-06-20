import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model with generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman.  Jawab 'Mohon Maaf pertanyaan tidak berhubungan dengan Kopi' jika diluar konteks kopi. Anda memiliki akses ke semua kopi dinusantara.""",
)

# Initialize chat session
chat_session = model.start_chat(
    history=[
        {
            "role": "model",
            "parts": [
                "Halo! 👋 Saya adalah barista di kedai kopi ini. 😊\n"
                "Apa yang bisa saya bantu untuk Anda? Apakah Anda mencari rekomendasi kopi atau ingin tahu tentang menu kami? ☕️\n"
            ],
        }
    ]
)

# Streamlit App
st.title("Kedai Kopi Virtual")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input and response handling
if prompt := st.chat_input("Say something"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    chat_session.history.append({"role": "user", "parts": [prompt]})

    # Get response from the model
    response = chat_session.send_message(prompt)

    # Add model response to history
    st.session_state.messages.append({"role": "model", "parts": [response.text]})
    chat_session.history.append({"role": "model", "parts": [response.text]})

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message['parts'][0])
    else:
        st.chat_message("assistant").write(message['parts'][0])
