import os
import sys
import pathlib
import time
import random
import string
import textwrap
import PIL.Image
import streamlit as st
from PIL import Image
import numpy as np
import google.generativeai as genai
import time
import numpy as np
import pandas as pd
import streamlit as st




#--------------------- Setting up API ----------------------------
@st.cache_data
def to_markdown(text):
                text = text.replace('•', '  *')
                return (textwrap.indent(text, '> ', predicate=lambda _: True))
#get your API key from "https://makersuite.google.com/app/apikey"
GOOGLE_API_KEY='AIzaSyDNuMTckAlnvEZjl57C-pO2oZPW4W3sbYw'
genai.configure(api_key=GOOGLE_API_KEY)




st.title("Automating your catalogue.")


# Create a file uploader widget with a label and accepted file types
uploaded_file = st.file_uploader("Upload your product image here...", type=['png', 'jpeg', 'jpg'])
# Check if the uploaded_file variable is None
if uploaded_file is None:
    # Stop the execution of the script

    st.stop()

image = Image.open(uploaded_file)
col1, col2, col3 = st.columns([0.2, 5, 0.2])
#col2.image(image, use_column_width=True)
# Display an image with a width of 400 pixels and clamp the pixels
col2.image(image, width=200, clamp=True)



#----------- Gemini Vision -----------------------
def vision():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)
    prompt = "You are a experienced and highly skilled copywriter who is expert at writing product titles, please write short and crisp product title. %s.please respond only with title of the product image i am providing you"
    response = model.generate_content(["What do you see in this image%s please respont only with main object text.", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text





def description():
    model = genai.GenerativeModel('gemini-pro')
    text = vision()
    prompt = ("You are a experienced and highly skilled copywriter who is expert at writing product descriptions, please write short and persuasive product description within 100 words %s.please respond only with description of the product i am providing you. take inspiration from this description" % text)
    response = model.generate_content(prompt)
    return response.text




def the_brand():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)    
    response = model.generate_content(["I provided you image of an product, you have to tell me brand of the product if visible in image.% please respond only with actual name, if no weights provided respond 'Image do not contains this information'", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text



def the_country():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)    
    response = model.generate_content(["I provided you image of an product, you have to search using info you have then tell me the country origin of the product.% please respond only with country name name, if you don't find country of origin please respod  'Not found :( Sorry, We’re in beta. Consider adding this manually, fixing it soon.'", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text



def the_weight():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)
    response = model.generate_content(["I provided you image of an product, you have to search using info you have then tell me the weight of the product.% please respond only with actual weight, if no weights provided respond  'Not found :( Sorry, We’re in beta. Consider adding this manually, fixing it soon.'", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text


def the_contact():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)    
    response = model.generate_content(["I provided you image of an prodect, please tell me only mobile number and email id of the brand making this product.% use image or your data to come up with details please respond only with actual email id and mobile number. if no details provided respond 'Not found :( Sorry, We’re in beta. Consider adding this manually, fixing it soon.'", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text



def generate_random_sku(length=12):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))









    
title = st.text_input('Title', vision())
Description = st.text_area('Description', description())
sku = st.text_input('SKU ID', generate_random_sku())
Country = st.text_input('Country of origin', the_country())
Brand = st.text_input('Brand', the_brand())
Weight = st.text_input('Weight',the_weight())
Instructions = st.text_input('Instructions','Please refer to the product')
Contact = st.text_input('Contact',the_contact())


st.stop()
