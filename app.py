
import streamlit as st
from backend import get_response, clear_history, get_history


st.set_page_config(
    page_title="IT Teacher",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# -----------------------------
# Minimal CSS
# -----------------------------

st.markdown("""
<style>

    /* Entire page */
    .stApp {
        background: #ffffff !important;
    }

    /* Remove Streamlit top decoration */
    header {
        background: #ffffff !important;
    }

    [data-testid="stHeader"] {
        background: #ffffff !important;
    }

    /* Main area */
    .block-container {
        max-width: 700px;
        padding-top: 45px;
        padding-bottom: 100px;
    }

    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Heading */
    .app-title {
        text-align: center;
        font-size: 24px;
        font-weight: 500;
        color: #111111;
        margin-bottom: 45px;
    }

    /* Normal text */
    p, li, span, label {
        color: #111111 !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 8px 0 !important;
    }

    /* Chat message text */
    [data-testid="stChatMessage"] p {
        color: #111111 !important;
        font-size: 15px;
        line-height: 1.6;
    }

    /* Remove chat avatars */
    [data-testid="stChatMessageAvatar"] {
        display: none;
    }

    /* Input container */
    [data-testid="stChatInput"] {
        background: white !important;
        border: 1px solid #dddddd !important;
        border-radius: 8px !important;
    }

    /* Input box */
    [data-testid="stChatInput"] textarea {
        background: white !important;
        color: #111111 !important;
        border: none !important;
        font-size: 15px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888 !important;
    }

    /* Remove focus colors */
    [data-testid="stChatInput"]:focus-within {
        border-color: #aaaaaa !important;
        box-shadow: none !important;
    }

    /* Remove bottom decoration */
    footer {
        display: none !important;
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Title
# -----------------------------

st.markdown(
    '<div class="app-title">IT Teacher</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Chat history
# -----------------------------

history = get_history()

for message in history:

    with st.chat_message(message["role"], avatar=None):
        st.markdown(message["content"])


# -----------------------------
# Input
# -----------------------------

user_message = st.chat_input("Ask something...")


# -----------------------------
# Generate response
# -----------------------------

if user_message:

    with st.chat_message("user", avatar=None):
        st.markdown(user_message)

    with st.chat_message("assistant", avatar=None):

        with st.spinner("Thinking..."):
            response = get_response(user_message)

        st.markdown(response)
