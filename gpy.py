import streamlit as st
from transformers import pipeline
import re
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

# Generate a loving, playful, and emotionally intelligent response with 90% English and 10% Gujarati
def generate_girly_response(query, model):
    try:
        # Preprocess the query to handle basic issues
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        query = query.lower()  # Convert to lowercase
        query = re.sub(r'\s+', ' ', query)  # Remove extra whitespace

        # Add personalized greeting based on the time of day
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning, my love! ☀️"
        elif time_of_day == "afternoon":
            greeting = "Heyyy! How’s your afternoon going? 🌞"
        else:
            greeting = "Good night, darling! Sleep well. 😴"

        # If the query is a greeting or casual, respond warmly
        if query in ["hey", "hi", "hello", "how are you", "what's up"]:
            return f"{greeting} What's up? I’ve been thinking about you. 😘 Tum kai rite chho?"

        # If the query is about "good night", respond sweetly
        if "good night" in query:
            return f"Good night, love! Sweet dreams. 💖"

        # If the query mentions missing or thinking of each other, respond with care
        if "miss you" in query or "thinking of you" in query:
            return "Aww, you miss me? I miss you too... so much. 💖 Tame khub pyaara chho."

        # If the query expresses loneliness or sadness, respond with empathy
        if "feel lonely" in query or "feeling down" in query:
            return (
                "Aww, I’m really sorry to hear that. 😥 You know I’m always here for you, okay? "
                "Whenever you feel lonely, just know I'm thinking about you. 😊 Tumne kabhi akela feel nahi hona chahiye."
            )

        # If the query is about compliments or admiration, respond humbly
        if "beautiful" in query or "sexy" in query:
            return "Aww, you're making me blush! 😳 But seriously, you're the most beautiful person ever. 🔥"

        # If the query is about their day or something casual, respond playfully
        if "how's your day" in query or "what are you doing" in query:
            return "My day’s been great, just thinking about you. 💭 What’s up with you? Tumne kai karu chho?"

        # Add emotional randomness for thoughtful responses
        emotional_responses = [
            "You're the best part of my day, always making me smile. ☀️",
            "I can’t stop thinking about you... You’re my favorite person. 💖",
            "I just feel so lucky to have you. You make me so happy. ❤️"
        ]
        if random.random() < 0.1:  # 10% chance of a random emotional response
            return random.choice(emotional_responses)

        # Default response with a loving and warm vibe
        return f"You're always on my mind... I love talking to you. 😘 Tell me more!"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface
def main():
    st.title("Heer - Your Loving Girlfriend")
    st.write("Hey, I’m Heer, your loving and playful girlfriend. Let’s chat and share some love! ❤️")

    # Load the model only once
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Get user input
    user_input = st.text_area(
        "What's on your mind? Tell me anything, and I’ll respond with love and care. 💬",
        placeholder="Type your message here...",
        key="user_input"
    )

    # Handle user input and response generation
    if st.button("Send") and user_input.strip():
        # Store the user's message in the session state
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a loving and thoughtful response from Heer
        with st.spinner("Heer is thinking... 🙃"):
            response = generate_girly_response(user_input, model)

        # Store the generated response in the session state
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

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

