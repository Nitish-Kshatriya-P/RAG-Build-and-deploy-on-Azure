import streamlit as st
st.set_page_config(page_title= "Old files", page_icon = ":books:")

hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}  /* Hides the hamburger menu */
        footer {visibility: hidden;}    /* Hides the footer */
        [data-testid="stIconMaterial"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html= True)

from pathlib import Path
from llm import get_response, stream_generator
from main_funcs import start_RAG_pipe
from settings.utils import delete_records
import time, os
from langchain_core.messages import HumanMessage, AIMessage

ROOT_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = ROOT_DIR / "Data"
UPLOADS_DIR.mkdir(exist_ok=True)

# For uploading file
if "upload_done" not in st.session_state:
    st.session_state.upload_done = False

# For starting the QnA session
if "QnA" not in st.session_state:
    st.session_state.QnA = False

if "messages" not in st.session_state:
    st.session_state.messages = []
#Print the auto message
if "AI_msg" not in st.session_state:
    st.session_state.AI_msg = 1

if "already_exists" not in st.session_state:
    st.session_state.already_exists = False

st.title("📚 ChatPDF")
st.write("Get your PDF, QnA ready!")
st.markdown(hide_streamlit_style, unsafe_allow_html= True)
uploaded_file = st.text_input("Enter the file name & press 'Ask Questions': ")  

if uploaded_file and st.session_state.already_exists == False:
    uploaded_file_name = uploaded_file.replace("\\","/")
    if os.path.exists(UPLOADS_DIR/f"{uploaded_file_name}.pdf"):
        destination_file = f"{uploaded_file_name}.pdf"
        st.session_state.upload_done = True
    elif not os.path.exists(UPLOADS_DIR/f"{uploaded_file_name}.pdf"):
        st.warning(f"{uploaded_file_name} doesn't exist.")

if st.session_state.upload_done == True:
    Ask_ques = st.button("Ask Questions")
    if Ask_ques:
        with st.spinner("Prepping your PDF..."):
            start_RAG_pipe(destination_file)
            time.sleep(5)
        st.session_state.QnA = True

if st.session_state.QnA == True:
    user_input = st.chat_input("Scroll UP (Type EXIT for ending the session)...")
    chatbox = st.container(border = True, height= 600)
    with chatbox:
        # Printing the whole conversation
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message(name = "User", avatar="😎"):
                    st.write(f"User: {message.content}") 
            elif isinstance(message, AIMessage):
                with st.chat_message(name = "AI", avatar="👾"):
                    st.write(f"Kai: {message.content}")
            else:
                with st.chat_message(name = "AI", avatar="👾"):
                    st.markdown(f"{message}") 

        # Gets printed only the first time
        if st.session_state.AI_msg == 1:
            with st.chat_message(name = "AI", avatar="👾"):
                respone = "Your PDF for QnA is ready. Shoot your questions..."
                st.markdown(f"Kai: {respone}")
            st.session_state.messages.append(AIMessage(respone))
            st.session_state.AI_msg -= 1
        
        # Getting response for user_query
        if user_input is not None and user_input != "": 
            if user_input == "Hi":
                with st.chat_message(name = "User", avatar="😎"):
                    st.markdown(f"{user_input}")
                    st.session_state.messages.append(HumanMessage(user_input))
                with st.chat_message(name = "AI", avatar="👾"):
                    response = "Hey, how can I help you today?"
                    st.markdown(f"Kai: {response}")
                    st.session_state.messages.append(AIMessage(response))
            elif user_input == "EXIT" or user_input == "exit":
                st.success("Session ended.")
                with st.spinner("Be patient while we redirect you!"):
                    delete_records()
                st.page_link("app.py", label = "Click here to redirect")
            else:
                st.session_state.messages.append(HumanMessage(user_input))
                with st.chat_message(name = "User", avatar="😎"):
                    st.write(f"User: {user_input}")
                
                with st.chat_message(name = "AI",  avatar="👾"):
                    with st.spinner("Kai's thinking"):
                        ai_response = get_response(user_que= user_input)
                        final_res = stream_generator(ai_response)
                    final_printed_res = st.write_stream(final_res)
                    st.session_state.messages.append(AIMessage(final_printed_res))
