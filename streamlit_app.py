import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# FastAPI URL (for the deployed backend)
API_URL = "http://localhost:8000/query/"

st.title("Titanic Dataset Chatbot")

# Create a simple input for the user to ask questions
user_question = st.text_input("Ask a question about the Titanic dataset:")

if user_question:
    response = requests.post(API_URL, json={"question": user_question})

    if response.status_code == 200:
        data = response.json()
        st.write(data['response'])

        # If an image URL is returned (for visualizations), display the image
        if 'image' in data:
            img_url = data['image']
            img = Image.open(img_url)
            st.image(img, caption="Titanic Dataset Visualization", use_column_width=True)

    else:
        st.write("Sorry, there was an error processing your query.")
