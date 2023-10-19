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
timeout = 60
url = getenv("url_backend")


def show_result(r):
    try:
        rs = r.json()
        if rs.get("result"):
            st.session_state.result = rs.get("result")
        else:
            st.error("something went wrong :(")
            st.session_state.error = True
    except:
        st.error("something went wrong :(")
        st.session_state.error = True


def request_data():
    st.session_state.result = []
    st.session_state.links = []
    if st.session_state.query:
        payload = {
            "query": st.session_state.query,
            "model_name": st.session_state.model,
        }
        if technique in ["ChatGPT", "ChatGPT-Vanilla"]:
            tq = "/askGPT"
            if technique == "ChatGPT-Vanilla":
                payload["concise"] = False
            else:
                payload["concise"] = True
        elif technique in ["RAG", "RAG+ChatGPT"]:
            tq = "/askRAG"
            if technique == "RAG+ChatGPT":
                payload["combined"] = True
            else:
                payload["combined"] = False
        else:
            tq = "/askPALM"
        async_request(
            "get",
            url + tq,
            json=payload,
            callback=lambda r: show_result(r),
        )

        with spinner.container():
            with st.spinner(text="generating response ..."):
                for seconds in range(timeout):
                    time.sleep(1)
                    if len(st.session_state.result) > 0 and not st.session_state.error:
                        st.empty()
                        break
                    elif st.session_state.error:
                        st.session_state.error = False
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
init_state_var("model", "GPT4(untuned)")
init_state_var(
    "technique",
    "RAG",
)
init_state_var(
    "error",
    False,
)

technique = st.sidebar.selectbox(
    "technique",
    ("RAG", "RAG+ChatGPT", "PALM", "ChatGPT", "ChatGPT-Vanilla"),
    index=0,
    key="technique",
)
if technique == "ChatGPT":
    model_disable = False
else:
    model_disable = True

model_select = st.sidebar.selectbox(
    "Model",
    ("GPT4(untuned)", "finetuned-gpt3.5(short)", "finetuned-gpt3.5(long)"),
    index=0,
    key="model",
    disabled=model_disable,
)


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
        for chunk in st.session_state.result.split('\n'):
            st.markdown(
                f'<div style="font-size:20px;">{chunk}</div>',
                unsafe_allow_html=True,
            )
        st.text(" ")
        st.text(" ")
    else:
        content.empty()
