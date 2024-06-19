import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List of coffee names
coffee_names = [
    "Aceh Gayo", "Sidikalang", "Samosir", "Simalungun", "Lintong", 
    "Mandheling", "Rangsang Meranti", "Tungkal Jambi", "Kerinci", 
    "Semendo", "Lampung", "Java Preanger", "Ciwidey", "Puntang", 
    "Sindoro Sumbing", "Temanggung", "Jampit", "Ijen Raung", 
    "Pupuan", "Kintamani", "Tambora", "Wae Rebo", "Bajawa", 
    "Sokoria", "Kubu Raya", "Kota Waringin", "Pinogo", 
    "Benteng Alla", "Toraja", "Enrekang", "Nabire", "Dogiyai", 
    "Cartenz", "Baliem Valley"
]

# Generative AI configuration
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
    system_instruction="Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman.  Jawab 'Mohon Maaf pertanyaan tidak berhubungan dengan Kopi' jika diluar konteks kopi. Anda memiliki akses ke semua kopi dinusantara.",
)

# Function to fetch fun fact
def fetch_fun_fact(coffee_name):
    question = f"Buat Fun Fact mengenai kopi {coffee_name}"
    response = model.generate_content("Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman. Jawab tanpa menambahkan pertanyaan baru. Jawab pertanyaan berikut: " + question)
    return response.text

# Function to generate blend tasting notes
def generate_blend_tasting_notes(coffee1, percentage1, coffee2, percentage2):
    blend_description = f"Buat deskripsi rasa dari campuran kopi {coffee1} ({percentage1}%) dan {coffee2} ({percentage2}%)"
    response = model.generate_content(
        "Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman. Jawab tanpa menambahkan pertanyaan baru. Jawab pertanyaan berikut: " + blend_description
    )
    return response.text

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
st.set_page_config(page_title="Kedai Kopi Virtual Nusantara", layout="wide")

# Sidebar for navigation
with st.sidebar:
    st.title("Navigasi")
    page = st.radio("Pilih halaman:", ["Fun Fact Kopi", "Deskripsi Campuran", "Obrolan Virtual"])

st.title("Kedai Kopi Virtual Nusantara")

if page == "Fun Fact Kopi":
    st.header("Fun Fact Kopi Nusantara")
    selected_coffee = st.selectbox("Pilih nama kopi:", coffee_names)
    if st.button('Tampilkan Fun Fact'):
        fun_fact = fetch_fun_fact(selected_coffee)
        st.write(fun_fact)

elif page == "Deskripsi Campuran":
    st.header("Deskripsi Rasa Campuran Kopi Nusantara")
    coffee1 = st.selectbox("Pilih kopi pertama:", coffee_names, key='coffee1')
    coffee2 = st.selectbox("Pilih kopi kedua:", coffee_names, key='coffee2')
    percentage1 = st.slider(f"Persentase {coffee1}:", 0, 100, 50, key='percentage1')
    percentage2 = 100 - percentage1
    st.write(f"Persentase {coffee2}: {percentage2}%")
    if st.button('Tampilkan Deskripsi Rasa'):
        tasting_notes = generate_blend_tasting_notes(coffee1, percentage1, coffee2, percentage2)
        st.write(tasting_notes)

elif page == "Obrolan Virtual":
    st.header("Obrolan Virtual dengan Barista")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if prompt := st.chat_input("Katakan sesuatu"):
        st.session_state.messages.append({"role": "user", "parts": [prompt]})
        chat_session.history.append({"role": "user", "parts": [prompt]})
        response = chat_session.send_message(prompt)
        st.session_state.messages.append({"role": "model", "parts": [response.text]})
        chat_session.history.append({"role": "model", "parts": [response.text]})
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message['parts'][0])
        else:
            st.chat_message("assistant").write(message['parts'][0])
