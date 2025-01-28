import streamlit as st
from transformers import pipeline
import random
from datetime import datetime

# Set up the Streamlit page configuration (must be the first command)
st.set_page_config(page_title="Heer - Your Loving Girlfriend", page_icon="❤️")

# Load the model (simplified version without any advanced caching)
@st.cache_resource
def load_model():
    try:
        # Load GPT-2 model for text generation
        return pipeline("text-generation", model="gpt2")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Helper function to determine the time of day
def get_time_of_day():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "night"

# Generate a more realistic, loving, and balanced response
def generate_girly_response(query, model):
    try:
        # Preprocess the query to handle basic issues
        query = query.lower()  # Convert to lowercase

        # Add personalized greeting based on the time of day
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning! I hope you're having a great start to your day."
        elif time_of_day == "afternoon":
            greeting = "Hey there! How’s your afternoon going?"
        else:
            greeting = "Good night! I hope you had a good day."

        # If the query is a greeting or casual, respond warmly and naturally
        if query in ["hey", "hi", "hello", "how are you", "what's up"]:
            return f"{greeting} I'm here if you want to talk. 😊"

        # If the query is about "good night", respond sweetly but not too flirty
        if "good night" in query:
            return f"Good night! Hope you sleep well and have sweet dreams."

        # If the query mentions missing or thinking of each other, respond with care
        if "miss you" in query or "thinking of you" in query:
            return "I miss you too. It's always nice to hear from you. Take care. 💖"

        # If the query expresses loneliness or sadness, respond with empathy
        if "feel lonely" in query or "feeling down" in query:
            return (
                "I'm really sorry you're feeling that way. It's okay to feel sad sometimes. "
                "Just remember you're not alone, and I'm always here if you need someone to talk to. 💖"
            )

        # If the query expresses mood swings, respond accordingly with understanding
        if "angry" in query or "frustrated" in query:
            return "I totally get how you feel. Sometimes things can be really frustrating, but you're strong. You'll get through this."

        if "sad" in query or "upset" in query:
            return "I'm sorry you're feeling like this. It’s okay to feel sad, but remember, things will get better. You're not alone."

        # If the query is about compliments or admiration, respond in a humble and friendly way
        if "beautiful" in query or "pretty" in query:
            return "Aww, you're so kind! But it's you who brightens my day. 😊"

        # If the query is about their day or something casual, respond thoughtfully
        if "how's your day" in query or "what are you doing" in query:
            return "My day’s going fine, just thinking about how you're doing. What about you?"

        # Default response with a supportive and friendly vibe
        return f"You're doing great. Let me know how I can make your day even better! 😊"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface
def main():
    # Set up custom styles for the chat UI
    st.markdown("""
        <style>
            .chat-box {
                max-width: 600px;
                margin: 0 auto;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 8px;
                height: 400px;
                overflow-y: scroll;
                margin-bottom: 20px;
            }
            .user-msg {
                background-color: #d1f7c4;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 5px;
                align-self: flex-start;
            }
            .heer-msg {
                background-color: #ffcccb;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 5px;
                align-self: flex-end;
            }
            .input-box {
                width: 100%;
                padding: 10px;
                background-color: #e9ecef;
                border-radius: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .input-text {
                border: none;
                background-color: #e9ecef;
                width: 90%;
                border-radius: 25px;
                padding: 10px;
            }
            .send-button {
                background-color: #ff6b6b;
                color: white;
                padding: 10px 20px;
                border-radius: 25px;
                border: none;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    # Set up Streamlit title and introduction
    st.title("Heer - Your Loving Girlfriend")
    st.write("Hey! I'm Heer, here to chat and keep you company. How’s your day going? 😊")

    # Load the model only once
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Input from the user (just one input field)
    user_input = st.text_input("Type your message...", key="user_input", placeholder="Type here...")

    # Button to send message
    if st.button("Send") and user_input.strip():
        # Store the user's message in the session state
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a loving and thoughtful response from Heer
        with st.spinner("Heer is thinking... 🙃"):
            response = generate_girly_response(user_input, model)

        # Store the generated response in the session state
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Clear input box after sending
        st.session_state.user_input = ""

    # Display the conversation history (messages stacked upwards)
    chat_box = st.container()
    with chat_box:
        chat_box = st.empty()
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-box"><div class="user-msg">{message["text"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-box"><div class="heer-msg">{message["text"]}</div></div>', unsafe_allow_html=True)

    # Footer for the app
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
