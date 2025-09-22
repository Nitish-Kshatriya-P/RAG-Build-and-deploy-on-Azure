import streamlit as st

hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}  /* Hides the hamburger menu */
        footer {visibility: hidden;}    /* Hides the footer */
        [data-testid="stIconMaterial"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html= True)

import keyboard
import os
from pathlib import Path
import time

path = "C:/Users/Admin/Desktop/LLMops/Data"

Pathe = Path("./Data/")

all_files = [file for file in Pathe.iterdir() if file.is_file()]

if "choice" not in st.session_state:
        st.session_state.choice = False

def new_pdf_uploaded():
    if "upload_pdf" not in st.session_state:
        st.session_state.upload_pdf = True

def old_pdf_uploaded():
    if "upload_pdf" not in st.session_state:
        st.session_state.upload_pdf = True

def pdf_uploaded():
    if "upload_pdf" not in st.session_state:
        st.session_state.upload_pdf = True

def started():
    if "started" not in st.session_state:
        st.session_state.started = True

@st.dialog(title ="With New or Existing file")
def end_choice():
    New_file, Old_file = st.columns(2, vertical_alignment= 'center')
    if New_file.button("New File to upload", key = "left"):
        st.switch_page("pages/New_upload.py")
    if Old_file.button("Check list of available files", key = "right"):
        for file in all_files:
            with st.chat_message(name = "AI", avatar="👾"):
                st.markdown(file.name.strip(".pdf"))
            time.sleep(1)
        st.success("Copy the file's name to Chat with...")
        #st.page_link("front-end/Already_uploaded_files.py", label = "Chat", icon = "😎")
        st.page_link("pages/Old_pdfs.py", label= "Click here to Chat!")
    
st.set_page_config(page_title="ChatPDF", page_icon = ":books:")

st.title("📚 ChatPDF")
st.write("Get your PDF, QnA ready!")

start, exit = st.columns(2, vertical_alignment= 'center', gap= "small")

# For strating the session
if start.button("Start", width= 'stretch'):
    end = st.session_state.choice = True
    if end:
        end_choice()

# For exiting
if exit.button("Quit App", width= 'stretch'):
    keyboard.press_and_release('ctrl+w')
    os._exit(0)