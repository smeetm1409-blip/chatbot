import streamlit as st

from backend import (
    get_response,
    clear_history,
    get_history
)


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Infa AI...",
    page_icon="💻",
    layout="centered"
)


# =========================================================
# Simple Styling
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background-color: white;
        color: black;
    }

    /* Main content width */
    .block-container {
        max-width: 800px;
        padding-top: 40px;
        padding-bottom: 40px;
    }

    /* Text */
    h1, h2, h3, p, label {
        color: black !important;
    }

    /* Chat messages */
    [data-testid="stChatMessage"] {
        background-color: white;
        border: 1px solid #dddddd;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background-color: white;
    }

    /* Buttons */
    .stButton button {
        background-color: white;
        color: black;
        border: 1px solid #cccccc;
        border-radius: 6px;
    }

    .stButton button:hover {
        border-color: #888888;
        color: black;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Header
# =========================================================

st.title("Infa AI")

st.write("Ask me anything about programming, IT, or computer science.")


# =========================================================
# Clear Button
# =========================================================

if st.button("Clear chat"):
    clear_history()
    st.rerun()


# =========================================================
# Display Conversation
# =========================================================

history = get_history()

for message in history:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    else:

        with st.chat_message("assistant"):
            st.write(message["content"])


# =========================================================
# Chat Input
# =========================================================

user_message = st.chat_input("Ask a question...")


if user_message:

    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_message)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):
            response = get_response(user_message)

        st.write(response)

    st.rerun()
