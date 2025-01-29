import streamlit as st
from transformers import pipeline
from datetime import datetime
import random
import requests
import time
from gtts import gTTS
import os
from io import BytesIO

# Set up Streamlit page config
st.set_page_config(page_title="Heer - Your Caring Girlfriend", page_icon="❤️", layout="wide")

# Load the GPT-Neo model for text generation
@st.cache_resource
def load_model():
    try:
        return pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
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
        
def get_random_image():
    access_key = 'FYUaCmniHOXHIndX89rRRPklRO9jO56TbAA45tMtuHI'
    
    # Expanding search categories to include more human-like, motivational, and emotional themes
    search_query = random.choice([
        'love', 'smile', 'comfort', 'positive', 'flowers', 'motivation', 
        'selfie', 'beauty', 'intimacy', 'cute animals', 'couple goals', 
        'romantic', 'adventure', 'travel', 'happiness', 'fun', 'relationships',
        'dreams', 'fashion', 'friendship', 'sexy', 'inspiration', 'family',
        'freedom', 'strength', 'peace', 'joy', 'good vibes', 'funny', 'positivity', 
        'laughter', 'hope', 'bliss', 'courage', 'gratefulness', 'wellness', 
        'mindfulness', 'success', 'creativity', 'believe', 'ambition', 
        'art', 'fitness', 'health', 'cozy', 'coffeelovers', 'winter', 'summer', 
        'autumn', 'spring', 'vacation', 'beach', 'sunset', 'sunrise', 'mountains', 
        'nature', 'stars', 'sky', 'clouds', 'love yourself', 'hugs', 'kisses', 
        'together', 'friends', 'self-care', 'vintage', 'romance', 'daydream', 
        'outdoors', 'wildlife', 'peaceful', 'travel the world', 'wanderlust', 
        'good morning', 'good night', 'family time', 'grateful', 'mindset', 'blessed',
        'wanderer', 'city life', 'urban', 'artistic', 'exploration', 'lifestyle', 
        'food', 'healthy living', 'happiness is', 'motivate yourself', 'fitness journey', 
        'creative ideas', 'inspired', 'wild', 'calm', 'independent', 'dream big'
    ])

    url = f"https://api.unsplash.com/photos/random?query={search_query}&client_id={access_key}"
    
    retry_count = 3
    for attempt in range(retry_count):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                images = response.json()  # Parse the JSON response
                image_url = random.choice(images)['urls']['regular']
                return image_url
            elif response.status_code == 24:
                print("Rate limit exceeded. Please try again later.")
                return None
            elif response.status_code == 5:
                print("Internal server error. Retrying...")
            elif response.status_code == 13:
                print(f"Bad request. Invalid query: {search_query}")
                return None
            elif response.status_code == 28:
                print("Request timeout. Retrying...")
            else:
                print(f"Error: {response.status_code} - Unable to fetch image")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        
        # Wait before retrying
        time.sleep(2)  # Wait for 2 seconds before retrying

    return None

# Example Usage:
image = get_random_image()
if image:
    print(f"Random Image URL: {image}")
else:
    print("Could not retrieve image.")

def generate_chat_response(query, model, user_name=None):
    try:
        query = query.lower()
        time_of_day = get_time_of_day()
        greeting = f"Hey, {user_name if user_name else 'babe'}! 💖"

        if "hi" in query or "hello" in query:
            return f"{greeting} Kaise ho? Aaj ka din kaisa chal raha hai?"
        if "how are you" in query:
            return f"Main theek hoon, thank you! Tum kaise ho, {user_name if user_name else 'babe'}? 🥰"
        if "sad" in query or "lonely" in query:
            return f"Arre, {user_name if user_name else 'babe'}, aise mat socho. Main tumhare saath hoon, tum akela nahi ho. 😢💖"
        if "good night" in query:
            return f"Good night, {user_name if user_name else 'babe'}! 🌙 Sapne acchi dekhna, aur kal milenge. 😴💋"
        if "miss you" in query:
            return f"Mujhe bhi tumhari yaad aati hai, {user_name if user_name else 'babe'}. Tum mere dil mein hamesha ho. 💕"
        if "how's your day" in query:
            return f"Mera din thoda boring tha, par tumse baat kar ke maza aa gaya. Tumhara din kaisa tha, {user_name if user_name else 'babe'}?"
        if "tell me a story" in query:
            return f"Ek baar ek ladki thi jo apne sapno ke peeche bhaag rahi thi... aur usne apna sapna sach kar liya. 😘 Tumhare sapne kya hain?"
        if "how was your day" in query:
            return f"Mera din thoda quiet tha, par tumhare saath baat kar ke dil khush ho gaya. Tumhare din ki baatein share karo! 🌸"
        if "call me" in query or "talk to me" in query:
            return f"Aww, tum mujhe call karna chahte ho? Tumhare saath baat kar ke mujhe hamesha acha lagta hai. 😊 Tumhare din ka kya scene tha?"

        if len(query.split()) < 3:
            return f"Thoda aur batao, {user_name if user_name else 'babe'}! Main tumse aur baat karna chahti hoon. 😘"
        
        return f"Yaar, tum kitne pyaare ho! 💖 Kuch aur baat karna chahoge?"

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to convert text to speech using gTTS (Google Text-to-Speech)
def text_to_speech(text):
    tts = gTTS(text=text, lang='hi')
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

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
                height: 500px;
                overflow-y: scroll;
                margin-bottom: 20px;
                display: flex;
                flex-direction: column;
            }
            .user-msg {
                background-color: #4a90e2;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 5px;
                align-self: flex-start;
                max-width: 75%;
            }
            .heer-msg {
                background-color: #f1c40f;
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
            .header {
                text-align: center;
                font-size: 24px;
                color: #f39c12;
                margin-bottom: 20px;
            }
            .profile-img {
                border-radius: 50%;
                width: 50px;
                height: 50px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Heer - Your Caring Girlfriend")
    st.write("Hey Jatan, I’m Heer. Let's chat! I'm here for you anytime. 💖")

    # Load the model
    model = load_model()
    if model is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Get user's name (optional)
    user_name = st.text_input("What's your name? (Optional)", "")

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
            response = generate_chat_response(user_input, model, user_name)

        # Store the generated response
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Convert the response to speech
        audio_file = text_to_speech(response)
        st.audio(audio_file, format='audio/mp3')

        # Optionally, get an image based on the conversation context
        if random.random() < 0.3:  # A small chance to share an image
            image_url = get_random_image()
            if image_url:
                st.image(image_url, caption="Here's something for you! 💖", use_column_width=True)

        # Manually clear the input field (without re-running the script)
        st.session_state.user_input = ""

    # Footer for the app
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
