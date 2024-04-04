import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

#Converting the image to bytes

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
    
#Initialize the streamlit app

st.set_page_config(page_title="Calorie Tracker App")

st.header("Calorie Tracker App")
uploaded_file = st.file_uploader("Choose an image of an invoice..",type=["jpg","png","jpeg"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded image",use_column_width=True)

submit = st.button("Tell me the nutritional value")

input_prompt = """You are an expert nutritionist where you need to see the items in the image and tell
                    the total calories of the foods shown in the image, also provide the details of
                    calories of food items based on the below format

                        1. Item 1 - no. of calories
                        2. Item 2 - no. of calories
                        ----
                        ----
                Finally you can also tell if the food is health or not and also mention
                the percentage content of proteins, carbohydrates, fat, fibers, sugar 
                and other things required in our diets """

#if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data)
    st.subheader("The response is..")
    st.write(response)