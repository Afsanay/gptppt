import base64
import io
import os
from PIL import Image
from pptx import Presentation
import streamlit as st
from io import BytesIO
from main import main
import requests
import zipfile
from image_gen import get_images

st.set_page_config(layout="wide")
st.title("GPT-PPT")

with st.sidebar:
    st.image(
        'https://imageio.forbes.com/specials-images/imageserve/5f51c38ba72e09805e578c53/3-Predictions-For-The-Role-Of'
        '-Artificial-Intelligence-In-Art-And-Design/960x0.jpg?format=jpg&width=960')
    st.title("GPT making your PPTs")

tab1, tab2, tab3 = st.tabs(["Topic", "Templates", "Generated PPT and Images"])

with tab1:
    topic = st.text_input(label="Topic Prompt", value=None, max_chars=100)
    API_KEY = st.secrets["API_KEY"]

template = None

def createPPT():
    with tab3:
        ppt = main(topic=topic, api_key=API_KEY, pages=5, template_path=template)
        urls = get_images(topic, API_KEY)
        cols = st.columns(len(urls))
        for i, col in enumerate(cols):
            with col:
                st.image(urls[i])
        zip_buf = BytesIO()
        with zipfile.ZipFile(file=zip_buf, mode='w', compression=zipfile.ZIP_DEFLATED) as z:
            for i, url in enumerate(urls):
                buf = BytesIO()
                image = Image.open(requests.get(url, stream=True).raw)
                image.save(buf, format="png")
                z.writestr(zinfo_or_arcname=f"image{i}.png", data=buf.getvalue())
                buf.close()
            buf = BytesIO()
            ppt.save(buf)
            z.writestr(zinfo_or_arcname="new_ppt.pptx", data=buf.getvalue())
        st.download_button(label="Download", data=zip_buf.getvalue(), file_name="response.zip")


with tab2:
    if template is None:
        n = len(os.listdir("images"))
        cols = st.columns(4)
        for i, col in enumerate(cols):
            with col:
                st.image(f"images/{i}.jpg")
                if st.button(label="click", key=i):
                    template = f"templates/{i}.pptx"
                    st.text("Selected Template")
                st.image(f"images/{i+4}.jpg")
                if st.button(label="click", key=i+4):
                    template = f"templates/{i+4}.pptx"
                    st.text("Selected Template")


    if topic != "None" and template is not None:
        st.button(label="Create", key=100, on_click=createPPT)
