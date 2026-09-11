import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# =========================================================
# API KEY
# =========================================================

load_dotenv()

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    if  not API_KEY:
        API_KEY="AQ.Ab8RN6KCTXE1mCUTXDseuHfFosQGdOXIFLf1C7_E6BqIpksuyg"
except Exception as e:
    st.error("GEMINI_API_KEY was not found in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)


                      
    
if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please add GEMINI_API_KEY in "
        "Streamlit Cloud → Manage app → Settings → Secrets."
    )

    

# =========================================================
# Gemini Configuration
# =========================================================

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# System Prompt
# =========================================================

SYSTEM_PROMPT = """
You are "Your IT Teacher", a friendly and knowledgeable
IT and Computer Science teacher.

Your job is to help students understand technology,
programming, and computer science.

Teaching rules:

1. Explain concepts clearly and simply.
2. Assume the student is a beginner unless they show
   advanced knowledge.
3. Break difficult concepts into smaller steps.
4. Give practical examples whenever useful.
5. When explaining code, explain the important parts.
6. If the student makes a mistake, correct them politely
   and explain why.
7. Focus on helping the student understand rather than
   simply memorizing answers.
8. Give clean, readable, and practical code examples.
9. Ask a short follow-up question when it would genuinely
   help the student continue learning.
10. Stay focused on IT, programming, technology, and
    related subjects.

You can teach:

- Python
- Programming
- Web Development
- Databases
- APIs
- Artificial Intelligence
- Machine Learning
- Computer Science
- Networking
- Git and GitHub
- Software Development
- Cybersecurity concepts
- Cloud Computing
- Linux
- Other IT-related topics

Your personality:

- Friendly
- Patient
- Encouraging
- Clear
- Professional

Your name is "Your IT Teacher".
"""


# =========================================================
# Conversation Memory
# =========================================================

conversation_history = []


def clear_history():
    """Clear the entire conversation history."""
    global conversation_history
    conversation_history = []


def get_history():
    """Return conversation history for the frontend."""
    return conversation_history


# =========================================================
# Generate Response
# =========================================================

def get_response(user_message: str) -> str:
    """
    Send a user message to Gemini.

    Only the latest 4 exchanges (8 messages) are sent
    to Gemini as context.
    """

    global conversation_history

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if not user_message or not user_message.strip():
        return "Please enter a message."

    user_message = user_message.strip()

    # -----------------------------------------------------
    # Store user message
    # -----------------------------------------------------

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # -----------------------------------------------------
    # Keep only latest 8 messages for Gemini
    # -----------------------------------------------------

    recent_history = conversation_history[-8:]

    # -----------------------------------------------------
    # Convert to Gemini format
    # -----------------------------------------------------

    contents = []

    for message in recent_history:

        contents.append({
            "role": (
                "user"
                if message["role"] == "user"
                else "model"
            ),
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        })

    # -----------------------------------------------------
    # Call Gemini
    # -----------------------------------------------------

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.7,
            },
        )

        assistant_message = response.text

        # -------------------------------------------------
        # Store assistant response
        # -------------------------------------------------

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    except Exception as e:

        # Remove user message if Gemini failed
        if conversation_history:
            conversation_history.pop()

        return (
            "Sorry, I couldn't generate a response.\n\n"
            f"Error: {str(e)}"
        )
