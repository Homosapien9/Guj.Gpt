import streamlit as st
from transformers import pipeline
import re
import random
from datetime import datetime

# Set up the Streamlit page configuration (must be first command in the script)
st.set_page_config(page_title="Heer - Your Teenage, Flirty BFF", page_icon="❤️")

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

# Generate a teenage-like loving, playful, and emotional response
def generate_teenage_response(query, model):
    try:
        # Preprocess the query to handle basic issues
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        query = query.lower()  # Convert to lowercase
        query = re.sub(r'\s+', ' ', query)  # Remove extra whitespace

        # Add personalized greeting based on the time of day
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning! 😴"
        elif time_of_day == "afternoon":
            greeting = "Heyyyy! What's up? 🌞"
        else:
            greeting = "Night, night! 🛏️ Don't forget to sleep... but... I'll miss you... 😜"

        # If the query is a greeting or casual, respond in a playful and casual way
        if query in ["hey", "hi", "hello", "how are you", "what's up"]:
            return f"{greeting} 😜 What's up? You look SO cute today, like seriously, I'm obsessed! 😍"

        # If the query is about "good night", respond in a cute, playful way
        if "good night" in query:
            return f"{greeting} 😘 Gonna dream about you all night... lucky me, right? 😈"

        # If the query mentions missing or thinking of each other, respond emotionally
        if "miss you" in query or "thinking of you" in query:
            return "You miss me? 😱 Awwww, I miss you too!! Like... a lot!! 💖 Why are you always on my mind?? 🥺💭"

        # If the query is a compliment, respond flirty and appreciative (teenage style)
        if "beautiful" in query or "sexy" in query:
            return "Stoppp!! 😳 You're gonna make me blush...! 💕 But seriously... you're EVERYTHING 😍🔥"

        # If the query is about their day or something casual, respond playfully and with curiosity
        if "how's your day" in query or "what are you doing" in query:
            return "Oh... just scrolling through my phone, like always 🙄 But now that you're here, I’m WAY more interested 😏"

        # Add emotional randomness for certain responses to simulate teenage-like behavior
        emotional_responses = [
            "Ughhh, you’re making me so happy right now!! 😭💖",
            "I just wanna spend EVERY second with you!! 😩💓",
            "OMG, why are you so perfect? 😍 I can't even!! 😵",
            "Why do I feel all warm and fuzzy inside when you talk to me? 🥺💖"
        ]
        if random.random() < 0.1:  # 10% chance of a random emotional response
            return random.choice(emotional_responses)

        # Default response (casual, playful)
        return f"Like, you seriously just know how to make me smile!! 😏 Tell me more, I'm super curious!! 💬"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface
def main():
    st.title("Heer - Your Teenage, Flirty BFF")
    st.write("Yo! I’m Heer, your super chill, super fun, and flirty teenage BFF. Let's chat! 😜💬")

    # Load the model only once
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Get user input
    user_input = st.text_area(
        "What's up? Type your message here, and I'll reply with some fun vibes and a lotta love! 💖",
        placeholder="Spill it! 🗣️",
        key="user_input"
    )

    # Handle user input and response generation
    if st.button("Send") and user_input.strip():
        # Store the user's message in the session state
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a human-like teenage response from Heer
        with st.spinner("Heer is thinking... 🙃"):
            response = generate_teenage_response(user_input, model)

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
