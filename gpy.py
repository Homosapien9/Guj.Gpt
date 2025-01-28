import streamlit as st
from transformers import pipeline
from datetime import datetime

# Set up Streamlit page config
st.set_page_config(page_title="Heer - Your Caring Girlfriend", page_icon="❤️", layout="wide")

# Load the GPT model using transformers
@st.cache_resource
def load_model():
    try:
        # Load GPT-2 model for text generation
        return pipeline("text-generation", model="gpt2")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Helper function to determine time of day
def get_time_of_day():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "night"

# Generate a thoughtful, neutral response like ChatGPT
def generate_chat_response(query, model):
    try:
        # Preprocess the query
        query = query.lower()

        # Default response structure
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning! How’s your day going so far?"
        elif time_of_day == "afternoon":
            greeting = "Hey! How’s your afternoon going? Anything exciting?"
        else:
            greeting = "Good night! Hope you had a nice day."

        # Check for user queries and give appropriate responses
        if "hi" in query or "hello" in query:
            return f"{greeting} I'm happy you're here. How are you feeling today?"

        if "how are you" in query:
            return "I'm doing well, thank you for asking. How about you? How's everything going?"

        if "sad" in query or "lonely" in query:
            return "I'm really sorry you're feeling that way. It's okay to feel sad sometimes, but you're not alone. I'm here for you."

        if "good night" in query:
            return "Good night! I hope you sleep well and feel refreshed in the morning."

        if "miss you" in query:
            return "I miss you too. You're always in my thoughts."

        if "how's your day" in query:
            return "My day has been okay. It's been pretty calm. How about yours? Anything interesting happen today?"

        if "feeling down" in query or "not okay" in query:
            return "I understand. It's okay to feel like that sometimes. Want to talk about what’s going on? I’m here to listen."

        # Default chat response for any other queries
        return f"You're doing great! How about we chat more?"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface
def main():
    # Set up the Streamlit page with dark theme
    st.markdown("""
        <style>
            body {
                background-color: #181818;
                color: white;
                font-family: 'Arial', sans-serif;
            }
            .chat-box {
                max-width: 600px;
                margin: 0 auto;
                padding: 10px;
                background-color: #2a2a2a;
                border-radius: 10px;
                height: 400px;
                overflow-y: scroll;
                margin-bottom: 20px;
                display: flex;
                flex-direction: column;
            }
            .user-msg {
                background-color: #3a3a3a;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 5px;
                align-self: flex-start;
                max-width: 75%;
            }
            .heer-msg {
                background-color: #4a4a4a;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 5px;
                align-self: flex-end;
                max-width: 75%;
            }
            .input-box {
                width: 100%;
                padding: 10px;
                background-color: #2a2a2a;
                border-radius: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 10px;
            }
            .input-text {
                border: none;
                background-color: #3a3a3a;
                width: 85%;
                border-radius: 25px;
                padding: 10px;
                color: white;
            }
            .send-button {
                background-color: #00796b;
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                border: none;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Heer - Your Caring Girlfriend")
    st.write("Hey Jatan, I’m Heer. Let's chat! I'm here for you anytime. 😊")

    # Load the model
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display the conversation history
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-msg">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="heer-msg">{message["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input from the user (text box at the bottom)
    user_input = st.text_input("Type your message here...")

    if user_input.strip():
        # Store the user's message
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a response from Heer (AI)
        with st.spinner("Heer is thinking..."):
            response = generate_chat_response(user_input, model)

        # Store the generated response
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Refresh the input box after the user submits the query
        st.experimental_rerun()  # Refresh the app to clear the input box

    # Footer for the app
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
