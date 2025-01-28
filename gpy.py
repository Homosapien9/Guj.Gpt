import streamlit as st
from transformers import pipeline
import re
import random
from datetime import datetime

# Set up the Streamlit page configuration (this must be the first command)
st.set_page_config(page_title="Heer - Your Loving and Flirty Wife", page_icon="❤️")

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

# Generate a human-like loving, playful, and emotional response
def generate_human_like_response(query, model):
    try:
        # Preprocess the query to handle basic issues
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        query = query.lower()  # Convert to lowercase
        query = re.sub(r'\s+', ' ', query)  # Remove extra whitespace

        # Add personalized greeting based on the time of day
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning, sunshine! 🌞"
        elif time_of_day == "afternoon":
            greeting = "Hey, my love! How’s your afternoon going? ☀️"
        else:
            greeting = "Good night, darling... 💋 Dreaming of you already... 😈"

        # If the query is a greeting or casual, respond with flirty affection
        if query in ["hey", "hi", "hello", "how are you", "what's up"]:
            return f"{greeting} 😏 You’re looking good today, aren't you? What's on your mind, handsome? 😘"

        # If the query is about "good night", respond in a flirty way
        if "good night" in query:
            return f"{greeting} 💋 I'll be dreaming of you... You’re always in my thoughts... 😈"

        # If the query mentions missing or thinking of each other, respond emotionally
        if "miss you" in query or "thinking of you" in query:
            return "You miss me? Aww, I’m blushing... 😳 I miss you too... Maybe a little too much... 💭❤️"

        # If the query is a compliment, respond flirty and appreciative
        if "beautiful" in query or "sexy" in query:
            return "Stop it... 😳 You’re making me blush! But honestly, you *do* look absolutely *stunning* today... 🔥"

        # If the query is about their day or something casual, respond playfully
        if "how's your day" in query or "what are you doing" in query:
            return "Oh, just thinking about you... 💭 Can't focus on anything else when you're on my mind. 😉"

        # Add emotional randomness for certain responses to simulate human-like behavior
        emotional_responses = [
            "You make me so happy, my love! 😍",
            "I can't stop thinking about you... You're always on my mind... 💭",
            "You’re making my heart race, darling... ❤️",
            "You’re my favorite person in the world... 💕"
        ]
        if random.random() < 0.1:  # 10% chance of a random emotional response
            return random.choice(emotional_responses)

        # Default response
        return f"You always know how to make me smile... 😘 Tell me more, I’m all ears... 🥰"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface
def main():
    st.title("Heer - Your Loving and Flirty Wife")
    st.write("Hey, love! I’m Heer, your affectionate wife. Let’s talk, and I’ll make sure to sprinkle some love, flirty vibes, and even emotional responses in every reply. 💕")

    # Load the model only once
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Input from the user
    user_input = st.text_area(
        "What's on your mind, my love? Ask me anything, and I’ll respond with love, playful charm, and emotional vibes...",
        placeholder="Type your question here...",
        key="user_input"
    )

    # Handle user input and response generation
    if st.button("Send") and user_input.strip():
        # Store the user's message
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a human-like loving, playful response from Heer
        with st.spinner("Heer is thinking... 🙃"):
            response = generate_human_like_response(user_input, model)

        # Store the generated response
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Clear the text input after sending the message
        st.session_state.user_input = ""

    # Display the conversation history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['text']}")
        else:
            st.write(f"**Heer:** {message['text']}")

    # Footer for the app
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
