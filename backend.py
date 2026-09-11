
import os
from dotenv import load_dotenv
from google import genai

# =========================================================
# Configuration
# =========================================================

load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError(
#         "GEMINI_API_KEY is not set. "
#         "Please create a .env file and add your Gemini API key."
#     )

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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
# In-Memory Conversation Storage
# =========================================================

conversation_history = []


def clear_history():
    """
    Clear the entire conversation history.
    """
    global conversation_history
    conversation_history = []


def get_history():
    """
    Return the complete conversation history.

    This is mainly used by the Streamlit frontend
    to display the conversation.
    """
    return conversation_history


# =========================================================
# Gemini Response Function
# =========================================================

def get_response(user_message: str) -> str:
    """
    Receive a user message, store it in memory,
    send the latest 4 conversation exchanges to Gemini,
    and return Gemini's response.
    """

    # -----------------------------------------------------
    # Validate input
    # -----------------------------------------------------

    if not user_message or not user_message.strip():
        return "Please enter a message."

    user_message = user_message.strip()

    # -----------------------------------------------------
    # Store user's message
    # -----------------------------------------------------

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # -----------------------------------------------------
    # MEMORY
    #
    # One exchange consists of:
    #
    # User      = 1 message
    # Assistant = 1 message
    #
    # Therefore:
    #
    # 4 exchanges = 8 messages
    #
    # We keep the entire conversation in memory,
    # but only send the latest 8 messages to Gemini.
    # -----------------------------------------------------

    recent_history = conversation_history[-8:]

    # -----------------------------------------------------
    # Convert our history into Gemini format
    # -----------------------------------------------------

    contents = []

    for message in recent_history:

        role = "user" if message["role"] == "user" else "model"

        contents.append({
            "role": role,
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
        # Store Gemini's response
        # -------------------------------------------------

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    # -----------------------------------------------------
    # Error handling
    # -----------------------------------------------------

    except Exception as e:

        # Remove the user message if Gemini failed.
        if conversation_history:
            conversation_history.pop()

        return (
            "Sorry, I couldn't connect to Gemini.\n\n"
            f"Error: {str(e)}"
        )
