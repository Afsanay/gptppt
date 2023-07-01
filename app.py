import base64
import os

from pptx import Presentation
import streamlit as st
from io import BytesIO
from main import main



st.set_page_config(layout="wide")
st.title("GPT-PPT")

topic = st.text_input(label="input", value=None, max_chars=100)
template = None
# placeholder = st.empty()
if template is None:
    # with placeholder.container():
    cols = st.columns(len(os.listdir("images")))
    for i, col in enumerate(cols):
        with col:
            st.image(f"images/{i}.jpg")
            if st.button(label="click", key=i):
                template = f"templates/{i}.pptx"
                st.text("Selected Template")

def createPPT():
    binary_output = main(topic=topic,pages=10,api_key="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",template_path=template)
    st.download_button(label='Download',
                       data=binary_output.getvalue(),
                       file_name='new_ppt.pptx')


if topic != "None" and template is not None:
    # with placeholder.container():
    st.button(label="Create",key=100,on_click=createPPT)
