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
genai.configure(api_key=os.environ['API_KEY'])




st.title("Launch Your Products Faster🚀")


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
    response = model.generate_content(["You are a digital catalogue maker your job is to analyse the image of product to be sold. you have to see and come up with relevant details about that product and respond with information about the product. %s please respond with information only", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text


def title():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)
    response = model.generate_content(["You are a catalogues digitizer for a online store, your job is to see image of the product and come up with short and SEO friendly product title and please do not include product weights in tile. %s please respont only with product title.", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text





def description():
    model = genai.GenerativeModel('gemini-pro')
    text = vision()
    prompt = ("You are a experienced and highly skilled copywriter who is expert at writing product descriptions, please write short and persuasive product description within 100 words %s.please respond only with description of the product i am providing you." % text)
    response = model.generate_content(prompt)
    return response.text





def benefits():
    model = genai.GenerativeModel('gemini-pro')
    text = vision()
    prompt = ("You are a experienced and highly skilled copywriter who is expert at writing product benefits, please write benefits of the product you are provided with %s. Keep it short and respond only with benefits of the product i am providing you." % text)
    response = model.generate_content(prompt)
    return response.text




def the_brand():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)    
    response = model.generate_content(["I provided you image of an product, you have to tell me brand of the product if visible in image.% please respond only with actual brand name, if no brand name provided respond with 'Image do not contains this information.'", img], stream=True)
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
    response = model.generate_content(["I provided you image of an product, you have to search using info you have then tell me the weight of the product.% please respond only with actual weight, if no weights provided respond  'Provided image do not contains this information.'", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text


def the_colour():
    img = PIL.Image.open(uploaded_file)
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(img)
    to_markdown(response.text)    
    response = model.generate_content(["You are a digital catalogue maker, I provided you image of an prodect, Tell me colour of this product, please only respond with actual colour. Only tell me if the information of colour is relevant to the product if the product is something wearable only then tell the colour otherwise say 'Information is not relevant for given product.'", img], stream=True)
    response.resolve()
    to_markdown(response.text)
    return response.text



def generate_random_sku(length=12):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))









sku = st.text_input('SKU ID', generate_random_sku())


with st.spinner('Generating title...'):
   titles = st.text_input('Title', title())




with st.spinner('Generating description...'):
    Description = st.text_area('Description', description())


with st.spinner('Identifying colour...'):
    Colour = st.text_input('Colour',the_colour())

with st.spinner('Filling brand...'):
    Brand = st.text_input('Brand', the_brand())

with st.spinner('Filling country...'):
    Country = st.text_input('Country of origin', the_country())

with st.spinner('Filling weights...'):
    Weight = st.text_input('Weight',the_weight())

with st.spinner('Writing benefits...'):
    Benefits = st.text_area('Product Benefits',benefits())



st.divider()

st.stop()
