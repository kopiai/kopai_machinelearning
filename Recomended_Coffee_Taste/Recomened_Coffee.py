import streamlit as st
import pickle
import h5py
import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to load the vectorizer from a pickle file
def load_vectorizer(file_path):
    with open(file_path, 'rb') as file:
        vectorizer = pickle.load(file)
    return vectorizer

# Function to load model from .h5 file
def load_model_from_h5(file_path, dataset_name):
    with h5py.File(file_path, 'r') as f:
        model_pickle = f[dataset_name][()]
    model = pickle.loads(model_pickle.tobytes())
    return model

# Load the SVM model
def load_svm_model(file_path):
    return load_model_from_h5(file_path, 'svm_recommendation')

# Load the TfidfVectorizer
vectorizer = load_vectorizer('vectorizer.pkl')

# Load data from Excel file
file_path = 'dataset.xlsx'
sheet1 = pd.read_excel(file_path, sheet_name='Sheet1')

# Load the SVM model
svm_model = load_svm_model('svm_model.h5')

# List of taste options
taste_options = [
    "Roasted Cacao", "Coriander", "Hazelnut", "Sandalwood", "Black Currant",
    "Silky", "Aromatic", "Wood", "Citrus", "Hint of Spice", "Butterscotch",
    "Apple", "Apricot", "Clove", "Jasmine", "Pronounced Citrus", "Syrupy",
    "Spices", "Chocolate Finish", "Dark Chocolate", "Hibiscus", "Gardenia",
    "Grapefruit Zest", "Strong Aroma", "Slight Nutty", "Juicy", "Clean",
    "Cherry", "Chocolaty", "Greeny", "Lemony", "Brown Sugar", "Caramel",
    "Nutty", "Spicy", "Herbal", "Yellow Fruits", "Fruity", "Honey", "Plum",
    "Earthy", "Tobacco", "Sweet", "Almond", "Peach", "Melon", "Salty",
    "Musk", "Walnut", "Orange Zest", "Raisin", "Black Cherry", "Pecan",
    "Herbs", "Lime", "Slightly Floral", "Lemon", "Black Tea", "Cinnamon",
    "Pomegranate", "Sarsaparilla", "Sweet Yam", "Vanilla", "Green Apple",
    "Smokey", "Honeylike"
]

# Function to recommend coffee based on input taste
def recommend_coffee(tastes):
    try:
        # Combine the selected tastes into a single string
        combined_taste = ' '.join(tastes)

        # Transform input taste using the loaded vectorizer
        taste_vector = vectorizer.transform([combined_taste])

        # Use SVM model for recommendation
        svm_scores = svm_model.predict_proba(taste_vector)[0]
        svm_top_indices = np.argsort(svm_scores)[-5:][::-1]

        svm_recommendations = []
        for index in svm_top_indices:
            svm_details = sheet1.iloc[index]
            svm_recommendations.append({
                'Type of Coffee': svm_details['Jenis Kopi'],
                'Name of Coffee': svm_details['Nama Kopi'],
                'Origin of Coffee': svm_details['Pulau'],
                'Altitude of Coffee': svm_details['Tinggi Penanaman']
            })

        return svm_recommendations

    except Exception as e:
        st.error(f"Error during recommendation: {e}")
        return []

# Streamlit App

st.title("Coffee Recommendation System")

# Multiselect for taste preferences
selected_tastes = st.multiselect(
    "Select up to 3 tastes that you prefer:",
    options=taste_options,
    default=None,
    max_selections=3
)

if st.button("Recommend Coffee"):
    if selected_tastes:
        recommendations = recommend_coffee(selected_tastes)
        st.subheader("Recommended Coffees:")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"**Recommendation {i}:**")
            for key, value in rec.items():
                st.markdown(f"- **{key}:** {value}")
            st.markdown("---")
    else:
        st.warning("Please select up to 3 tastes.")
