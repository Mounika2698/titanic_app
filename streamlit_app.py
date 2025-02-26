import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# FastAPI backend URL
API_URL = "https://titanic-app-x3q8.onrender.com/ask_question/"

# Streamlit UI
st.title("Titanic Dataset Chatbot")

# User input question
user_question = st.text_input("Ask a question about the Titanic dataset:")

if user_question:
    # Send the user question to the FastAPI server
    response = requests.post(API_URL, json={"query": user_question})
    response_data = response.json()

    # Display the textual answer
    st.subheader("Response:")
    st.write(response_data["answer"])

    # Check if there is an image (base64 encoded)
    if "image" in response_data:
        img_data = base64.b64decode(response_data["image"])
        img = Image.open(BytesIO(img_data))
        st.image(img, caption="Titanic Dataset Visualization", use_column_width=True)
