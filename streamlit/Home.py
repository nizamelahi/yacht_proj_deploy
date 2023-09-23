import streamlit as st
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

st.markdown(
    '<div style="text-align: center;color:#1b9acb;font-size:65px;vertical-align:top;">Welcome to Yacht GPT </div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align: center;font-size:20px  ;vertical-align:top;">Yacht GPT is your friendly AI guide knowledgeable in all things boat related. Want pointers on boat financing? Looking for maintenance tips? Hurricane prep? Give Yacht GPT a go!</div>',
    unsafe_allow_html=True,
)
