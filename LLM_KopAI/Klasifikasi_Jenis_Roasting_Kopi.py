import streamlit as st
import google.generativeai as genai
import PIL.Image
import os

from dotenv import load_dotenv
# Konfigurasi API Key untuk Google Generative AI
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Header aplikasi
st.title("Klasifikasi Jenis Roasting Kopi")
st.write("Unggah gambar biji kopi dan kami akan mengklasifikasikannya ke dalam jenis roasting: Light Roast, Medium Roast, Medium-Dark Roast, atau Dark Roast.")

# Fungsi untuk klasifikasi gambar
def classify_image(image):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([
        "Bertindaklah sebagai barista di sebuah kedai kopi yang nyaman. Jawab tanpa menambahkan pertanyaan baru. Jawab pertanyaan dengan pilihan Light Roast, Medium Roast, Medium-Dark Roast, dan Dark Roast. Jika gambar tidak mengandung biji kopi maka jawab dengan 'Maaf Gambar bukan termasuk Biji Kopi'. Klasifikasikan Jenis Roasting Kopi berdasarkan gambar yang dikirimkan."
    , image])
    return response.text

# Unggah gambar
uploaded_file = st.file_uploader("Unggah gambar biji kopi", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Tampilkan gambar yang diunggah
    image = PIL.Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diunggah", use_column_width=True)
    
    # Proses klasifikasi
    st.write("Mengklasifikasikan gambar...")
    classification = classify_image(image)
    st.write("Hasil Klasifikasi:", classification)
else:
    st.write("Harap unggah gambar biji kopi untuk diklasifikasikan.")

