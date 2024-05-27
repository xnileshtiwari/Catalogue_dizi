import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI 
from crewai import Crew
from dotenv import load_dotenv
import google.generativeai as genai
import os
from crewai import Agent, Crew, Process, Task
from PIL import Image
from PIL import ImageFile
from streamlit_image_select import image_select
ImageFile.LOAD_TRUNCATED_IMAGES = True
from catalogue_agent import Catalogueagent
from catalogue_task import Cataloguetask
import asyncio
import requests  # pip install requests

from streamlit_lottie import st_lottie


# Create and set an event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


st.title("Hi! I'm 🤖 your catalogue writer!")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


my_lottie = load_lottieurl("https://lottie.host/3ee79ca8-1219-4f16-b52c-7285c9d0bae2/GmNDbWPegL.json")

col1, col2, col3 = st.columns(3)
with col2:
    st.lottie(
        my_lottie,
        height = "250px",
        width = "250px"
        
    )


# st.set_page_config(page_icon="🚀")



def vision_tool(photo):
    api_key = os.environ.get('GOOGLE_API_KEY')
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    img =Image.open(photo)
    response = model.generate_content(["What is the name of product in image? Please respond with actual name only", img], stream = True)
    response.resolve()
    #return response.candidates[0]
    output = response.text
    return output





load_dotenv()




genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

llm = llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.4,
)


img1 = "Screenshot 2024-05-26 041052.png"
img2 = "Screenshot 2024-05-26 041126.png"
img3 = "chy.jpg"

# Create three columns
col1, col2, col3 = st.columns(3)

# Display images in each column
with col1:
    st.image(img1, caption="Image 1", use_column_width=True)

with col2:
    st.image(img2, caption="Image 2", use_column_width=True)

with col3:
    st.image(img3, caption="Image 3", use_column_width=True)


st.subheader("Drag and drop one of these images to see agents in action⚡")


# selected_image = image_select('label',["shirt.jpg", "jacket.webp","chy.jpg"])
# st.write(selected_image)


with st.form("Upload Images"):


    # File uploader for multiple images
    photo = st.file_uploader("Choose images", )


    submitted = st.form_submit_button("Submit")

if submitted:
    # Code to execute after submit button is clicked
    with st.spinner('Running agents...'):
        product = vision_tool(photo)

        agents = Catalogueagent()
        task = Cataloguetask()


        researcher = agents.researcher(llm)
        seo = agents.seo_expert(llm)
        writer = agents.writer(llm)




        research = task.researcher(product, researcher)
        key_words = task.research_seo(seo, product, research)
        writing = task.writing(writer, research, key_words, product)






        crew = Crew(
        agents=[
        researcher,
        seo,
        writer,
        ],
        tasks=[
        research,
        key_words,
        writing
        ],
        verbose=True,
        
        process=Process.sequential,
        )
            


        result = crew.kickoff()
        container = st.container(border=True)

        container.write(result)




