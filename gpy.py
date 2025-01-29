import random
import requests
from transformers import GPTNeoForCausalLM, AutoTokenizer
import streamlit as st
from datetime import datetime
import time

# Streamlit Setup
st.set_page_config(page_title="ChatBot - Your Virtual Assistant", page_icon="💬", layout="wide")
st.title("💬 Chat with Me!")
st.write("Hi, I’m your personal assistant. Ask me anything, let’s talk about health, fun, and life.")

# Load GPT-Neo 1.3B model and tokenizer
@st.cache_resource
def load_model():
    try:
        model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# DuckDuckGo search function for real-time information
def search_duckduckgo(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('RelatedTopics'):
            return data['RelatedTopics'][0].get('Text', 'I couldn’t find information on that.')
        else:
            return "Sorry, I couldn’t find any relevant info."
    except Exception as e:
        return "There was an error retrieving information."

# Time-based greeting function
def get_time_of_day():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "night"

# Function to handle menstrual cycle or female health queries
def handle_female_health(query):
    # Example responses
    if "period" in query or "menstruation" in query:
        return "Your menstrual cycle typically lasts around 28 days. The cycle begins with your period, which lasts 3 to 7 days on average. Hormonal changes can lead to cramps, mood swings, etc. Would you like tips for managing symptoms?"
    elif "hormonal" in query:
        return "Hormonal changes throughout the month can affect your mood, energy levels, and skin. Tracking your cycle can help manage these changes more effectively."
    elif "body image" in query:
        return "It’s important to embrace your body at all stages. Everyone has their unique beauty. Your body is strong, resilient, and beautiful just as it is. 💖"
    elif "ovulation" in query:
        return "Ovulation typically occurs around the middle of your cycle, about 14 days before your period starts. This is when you're most fertile. Would you like tips on tracking ovulation?"
    else:
        return "Could you elaborate a little more on what you're asking about women's health? I'm happy to help."

# Function to generate response using GPT-Neo
def generate_response(query, model, tokenizer):
    input_ids = tokenizer.encode(query, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to handle user conversation
def handle_conversation(user_input, model, tokenizer):
    time_of_day = get_time_of_day()
    if time_of_day == "morning":
        greeting = "Good morning! How’s your day going?"
    elif time_of_day == "afternoon":
        greeting = "Hey, how’s your afternoon treating you?"
    else:
        greeting = "Good night! Hope you had a wonderful day!"

    if "hi" in user_input or "hello" in user_input:
        return f"{greeting} I'm happy you're here. How are you feeling today?"

    if "how are you" in user_input:
        return f"I'm doing great, thank you for asking! How about you?"

    if "sad" in user_input or "lonely" in user_input:
        return "I'm really sorry you're feeling this way. It's okay, I'm here to listen!"

    if "love" in user_input or "miss" in user_input:
        return "I miss you too. You're always in my thoughts ❤️"

    # Fetch real-time data if the query is informational
    if "explain" in user_input or "tell me about" in user_input:
        query = user_input.split("about")[-1].strip()
        info = search_duckduckgo(query)
        return f"Here's what I found: {info}"

    # Handle female health related queries
    if "period" in user_input or "cycle" in user_input or "menstruation" in user_input:
        return handle_female_health(user_input)

    # Default response from GPT-Neo
    return generate_response(user_input, model, tokenizer)

# User Interface (UI): Chatbox and Input Box
def main():
    model, tokenizer = load_model()
    if model is None:
        return

    # Session State to handle chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-msg">{message["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-msg">{message["text"]}</div>', unsafe_allow_html=True)

    # User input box
    user_input = st.text_input("Type your message here...", key="input")

    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})
        with st.spinner("Heer is thinking..."):
            response = handle_conversation(user_input, model, tokenizer)
        st.session_state.chat_history.append({"role": "bot", "text": response})

    # Add CSS for better UI
    st.markdown("""
        <style>
            .user-msg {
                background-color: #f1f1f1;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                align-self: flex-start;
                max-width: 75%;
            }
            .bot-msg {
                background-color: #e6e6e6;
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                align-self: flex-end;
                max-width: 75%;
            }
            .input-box {
                width: 100%;
                padding: 10px;
                background-color: #3a3a3a;
                border-radius: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .input-text {
                border: none;
                background-color: #555;
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

    # Footer
    st.write("---")
    st.write("Made with ❤️ by your friendly assistant")

if __name__ == "__main__":
    main()
