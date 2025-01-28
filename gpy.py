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

# Generate a loving, playful, and emotionally intelligent response with 100% English
def generate_girly_response(query, model):
    try:
        # Preprocess the query to handle basic issues
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        query = query.lower()  # Convert to lowercase
        query = re.sub(r'\s+', ' ', query)  # Remove extra whitespace

        # Add personalized greeting based on the time of day
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning, my love! ☀️ How did you sleep?"
        elif time_of_day == "afternoon":
            greeting = "Hey, how’s your afternoon going? 🌞"
        else:
            greeting = "Good night, darling! Sleep tight. 😴"

        # If the query is a greeting or casual, respond warmly
        if query in ["hey", "hi", "hello", "how are you", "what's up"]:
            return f"{greeting} What's on your mind today? I'm here to listen. 😊"

        # If the query is about "good night", respond sweetly
        if "good night" in query:
            return f"Good night, love! Wishing you peaceful dreams. 💤 See you tomorrow!"

        # If the query mentions missing or thinking of each other, respond with care
        if "miss you" in query or "thinking of you" in query:
            return "I miss you too. It's always nice to hear from you. Take care, okay? 💖"

        # If the query expresses loneliness or sadness, respond with empathy
        if "feel lonely" in query or "feeling down" in query:
            return (
                "I’m really sorry you're feeling that way. 😔 It’s okay to feel down sometimes. "
                "Just know you’re not alone, and I’m always here if you need someone to talk to. 💖"
            )

        # If the query expresses mood swings, respond accordingly
        if "angry" in query or "frustrated" in query:
            return (
                "I get it... Sometimes life can be so frustrating. 😤 But hey, you’re strong and you’ll get through this, okay?"
            )
        if "sad" in query or "upset" in query:
            return (
                "Aw, I’m sorry you’re feeling down. 😔 But it’s okay, everyone has those days. I’m here for you. 💖"
            )

        # If the query is about compliments or admiration, respond humbly and sweetly
        if "beautiful" in query or "pretty" in query:
            return "Thank you, you’re so sweet! But honestly, it’s you who makes everything better. 😊"

        # If the query is about their day or something casual, respond thoughtfully
        if "how's your day" in query or "what are you doing" in query:
            return "My day’s going well, just thinking about you. How about yours? What did you do today?"

        # Add random supportive responses that are thoughtful
        emotional_responses = [
            "You’re such a wonderful person, and I’m so lucky to have you in my life. 💕",
            "I hope you know how much you mean to me. You make my world brighter. 🌟",
            "You’re strong and amazing, even on the tough days. I’m proud of you. 💖",
            "Whenever you need to talk, I’m always here. I’ve got your back. 😊"
        ]
        if random.random() < 0.1:  # 10% chance of a random emotional response
            return random.choice(emotional_responses)

        # Default response with a loving and supportive vibe
        return f"You’re such a great person. I’m always happy to chat with you. 😊 Tell me more about how you’re doing!"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface
def main():
    # Set the background style to give a WhatsApp-like feel
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

    st.title("Heer - Your Loving Girlfriend")
    st.write("Hey, I’m Heer! I’m here to chat with you, share love, and make your day brighter. ❤️")

    # Load the model only once
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Handle user input and response generation
    user_input = st.text_input("Type here...", key="user_input")

    if st.button("Send") and user_input.strip():
        # Store the user's message in the session state
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a loving and thoughtful response from Heer
        with st.spinner("Heer is thinking... 🙃"):
            response = generate_girly_response(user_input, model)

        # Store the generated response in the session state
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Clear input box
        st.session_state.user_input = ""

    # Display the conversation history with WhatsApp-like bubble design
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-msg">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="heer-msg">{message["text"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input and send button at the bottom
    st.markdown("""
        <div class="input-box">
            <input class="input-text" type="text" placeholder="Type your message..." id="user_input" value="">
            <button class="send-button">Send</button>
        </div>
    """, unsafe_allow_html=True)

    # Footer for the app
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
