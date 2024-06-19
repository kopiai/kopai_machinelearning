import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_blend_tasting_notes(coffee1, percentage1, coffee2, percentage2):
    model = genai.GenerativeModel('gemini-1.5-flash')
    blend_description = f"Buat deskripsi rasa dari campuran kopi {coffee1} ({percentage1}%) dan {coffee2} ({percentage2}%)"
    response = model.generate_content(
        "Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman. Jawab tanpa menambahkan pertanyaan baru. Jawab pertanyaan berikut: " + blend_description
    )
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
st.title("Deskripsi Rasa Campuran Kopi Nusantara")

# Dropdowns for selecting coffee types
coffee1 = st.selectbox("Pilih kopi pertama:", coffee_names)
coffee2 = st.selectbox("Pilih kopi kedua:", coffee_names)

# Sliders for selecting percentages
percentage1 = st.slider(f"Persentase {coffee1}:", 0, 100, 50)
percentage2 = 100 - percentage1  # Automatically adjust the second percentage
st.write(f"Persentase {coffee2}: {percentage2}%")

# Fetch Blend Tasting Notes
if st.button('Tampilkan Deskripsi Rasa'):
    tasting_notes = generate_blend_tasting_notes(coffee1, percentage1, coffee2, percentage2)
    st.write(tasting_notes)
