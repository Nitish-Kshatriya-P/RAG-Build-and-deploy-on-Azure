import streamlit as st
from pathlib import Path
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Streamlit app...")

# Hide Streamlit UI elements
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stIconMaterial"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Set page config
st.set_page_config(page_title="ChatPDF", page_icon=":books:")

# Directory setup
path = "./Data"
try:
    Path(path).mkdir(exist_ok=True)
    logger.info(f"Created directory {path}")
except Exception as e:
    logger.error(f"Failed to create directory {path}: {e}")
    st.error(f"Error creating directory {path}: {e}")

# List files
try:
    all_files = [file for file in Path(path).iterdir() if file.is_file()]
    logger.info(f"Found {len(all_files)} files in {path}")
except Exception as e:
    logger.error(f"Failed to list files in {path}: {e}")
    st.error(f"Error listing files: {e}")
    all_files = []

# Session state
if "choice" not in st.session_state:
    st.session_state.choice = False

def pdf_uploaded():
    st.session_state.upload_pdf = True
    logger.info("Set upload_pdf to True")

def started():
    st.session_state.started = True
    logger.info("Set started to True")

@st.dialog(title="With New or Existing file")
def end_choice():
    New_file, Old_file = st.columns(2, vertical_alignment='center')
    if New_file.button("New File to upload", key="left"):
        try:
            st.switch_page("pages/New_upload.py")
        except Exception as e:
            logger.error(f"Failed to switch to New_upload.py: {e}")
            st.error(f"Error navigating to New Upload: {e}")
    if Old_file.button("Check list of available files", key="right"):
        if not all_files:
            st.warning("No files found in Data directory")
            logger.warning("No files found in Data directory")
        for file in all_files:
            with st.chat_message(name="AI", avatar="👾"):
                st.markdown(file.name.strip(".pdf"))
            time.sleep(1)
        st.success("Copy the file's name to Chat with...")
        try:
            st.page_link("pages/Old_pdfs.py", label="Click here to Chat!")
        except Exception as e:
            logger.error(f"Failed to link to Old_pdfs.py: {e}")
            st.error(f"Error linking to Old PDFs: {e}")

# Main UI
try:
    st.title("📚 ChatPDF")
    st.write("Get your PDF, QnA ready!")

    start, exit = st.columns(2, vertical_alignment='center', gap="small")

    if start.button("Start", width='stretch'):
        logger.info("Start button clicked")
        st.session_state.choice = True
        end_choice()

    if exit.button("Quit App", width='stretch'):
        logger.info("Quit App button clicked")
        st.write("Exiting app...")
        st.stop()
except Exception as e:
    logger.error(f"Error rendering main page: {e}")
    st.error(f"Error rendering page: {e}")

logger.info("Streamlit app ready")