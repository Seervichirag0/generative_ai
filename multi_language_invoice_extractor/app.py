from dotenv import load_dotenv

load_dotenv()  #load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Funtion to load gemini pro vision
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
                {
                "mime_type": uploaded_file.type,  #Get the mime type of the image uploaded
                "data": bytes_data  
                }
            ]
            
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


#initialize your streamlit app

st.set_page_config(page_title="Multi Language invoice extractor")

st.header("Multi Language invoice extractor")
input = st.text_input("Input_text",key='input')
uploaded_file = st.file_uploader("Choose an image of an invoice..",type=["jpg","png","jpeg"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = '''You are an expert in understanding invoices in various languages
We will upload an image as invoices and you will have to answer any questions
based on the uploaded invoice image
you also are able to check all the important details in the invoice such as names, addresses, product, quanties,
price, services, consulting, discount, etc.'''

#if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is..")
    st.write(response)