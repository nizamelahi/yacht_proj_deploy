import streamlit as st
from functions import async_request, init_state_var
import time
from os import getenv
from dotenv import load_dotenv

st.set_page_config(
    page_title="Yacht GPT",
    page_icon="🛥",
    layout="wide",
    initial_sidebar_state="expanded",
)
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

load_dotenv()
timeout = 30
url = getenv("url_backend")



def show_result(r):
    st.session_state.result = r.get("result")

def request_data():
    st.session_state.result = []
    st.session_state.links = []
    if st.session_state.query:
        payload = {"query": st.session_state.query,"model":st.session_state.model}
        async_request(
            "get",
            url + "/ask",
            json=payload,
            callback=lambda r: show_result(r.json()),
        )
        
        with spinner.container():
            with st.spinner(text="please wait"):
                for seconds in range(timeout):
                    time.sleep(1)
                    if len(st.session_state.result) > 0:
                        st.empty()
                        break
                if seconds == timeout - 1:
                    st.error("something went wrong :(")
    else:
        st.error("please enter prompt")


st.markdown(
    '<div style="text-align: center;color:#1b9acb;font-size:60px;vertical-align:top;">Yacht GPT</div>',
    unsafe_allow_html=True,
)

init_state_var("result", [])
init_state_var("model", False)

model_btn=st.sidebar.toggle("fine tuned model",key="model")

prompt_input = st.text_input(
    placeholder="Ask me anything!",
    label="search request",
    key="query",
    label_visibility="hidden",
)

generate = st.button("Ask", type="primary")

spinner = st.empty()
content = st.empty()
nav = st.empty()


if generate:
    request_data()

with content.container():
    if len(st.session_state.get("result")) > 0:
            st.markdown(
                f'<div style="font-size:20px;vertical-align:top;">{st.session_state.result}</div>',
                unsafe_allow_html=True,
            )
            st.text(" ")
            st.text(" ")
    else:
        content.empty()
