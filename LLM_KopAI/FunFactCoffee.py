import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def fetch_fun_fact(coffee_name):
    model = genai.GenerativeModel('gemini-1.5-flash')
    question = f"Buat Fun Fact mengenai kopi {coffee_name}"
    response = model.generate_content("Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman. Jawab tanpa menambahkan pertanyaan baru. Jawab pertanyaan berikut: " + question)
    return response.text

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

# Streamlit App
st.title("Fun Fact Kopi Nusantara")

# Dropdown for selecting coffee name
selected_coffee = st.selectbox("Pilih nama kopi:", coffee_names)

# Fetch Fun Fact
if st.button('Tampilkan Fun Fact'):
    fun_fact = fetch_fun_fact(selected_coffee)
    st.write(fun_fact)
