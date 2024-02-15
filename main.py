import os
import random
import time
import string
import streamlit as st
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import google.generativeai as genai
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

st.title("Launch Your Products Faster🚀")
st.write("Please Reload if you are having any error!")


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





def generate(ques):
    api_key = os.environ.get('API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    img =Image.open(uploaded_file)
    response = model.generate_content([ques, img], stream = True)
    response.resolve()
    #return response.candidates[0]
    output = response.text
    return output



price = ("See the image and identify the price of the item. and read what is the price of the item if given. please respond with only price. if price is not given respond with 'Info not available in image' ")
title =("You are a catalogues digitizer for a online store, your job is to see image and read texts to identify the product and come up with short and SEO friendly product title and please do not include product weights in title.")
description= ("Imagine you are a product photographer and writer working for an online shopping platform. You are given the attached image of an unknown product. Your task is to identify the product accurately and write a clear and concise product description that would be helpful for potential buyers")
the_brand =("I provided you image of an product, please see the image, read the texts and predict the brand name of the product you have to tell me brand of the product if visible in image.% please respond only with actual brand name, if no brand name provided respond with 'Image do not contains this information'")
the_country = ("I provided you image of an product, see image and read the texts and search using info you have then tell me the country origin of the product.% please respond only with country name name, if you don't find country of origin please respod  'Not found :( Sorry, We’re in beta. Consider adding this manually, fixing it soon.'")
the_weight =("I provided you image of an product, please read the texts to identify the weight, if not written search using info you have then tell me the weight of the product.% please respond only with actual weight, if no weights provided respond  'Provided image do not contains this information.'")
benefits =("You are a experienced and highly skilled copywriter, see the image read the texts on object and write benefits of the product%s. Keep it short and respond only with benefits of the product i am providing you.")


def generate_random_sku(length=12):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


sku = st.text_input('SKU ID', generate_random_sku())
with st.spinner('Generating...'):
    titles = st.text_input('Title', generate(title))
with st.spinner('Generating...'):
    Description = st.text_area('Description',generate(description))
with st.spinner('Generating...'):
    Brand = st.text_input('Brand', generate(the_brand))
with st.spinner('Generating...'):
    Country = st.text_input('Country of origin', generate(the_country))
with st.spinner('Generating...'):
    price = st.text_input('Price', generate(price))
with st.spinner('Generating...'):
    Weight = st.text_input('Weight',generate(the_weight))
with st.spinner('Generating...'):
    Benefits = st.text_area('Product Benefits',generate(benefits))

st.divider()
