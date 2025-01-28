import streamlit as st
from transformers import pipeline
import torch
import re

# Load the model (with caching to prevent reloading on each run)
@st.cache_resource
def load_model():
    try:
        return pipeline("text-generation", model="gpt2")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Generate a cheeky and playful response
def gujinlish_heer_gpt(query, model):
    try:
        # Preprocess the query to handle typos and other errors
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        query = query.lower()  # Convert to lowercase
        query = re.sub(r'\s+', ' ', query)  # Remove extra whitespace

        # If the query is just a greeting or a simple "Hey", respond with playful affection
        if query in ["hey", "hi", "hello", "how are you", "what's up", "howdy"]:
            return "Well, hello there... 😏 Feeling lucky today? 😉 What’s on your mind, handsome?"

        # If the query is playful, respond with some cheeky comments
        if "good night" in query:
            return "Good night, my love... 💋 Don’t forget, I’ll be waiting for you in my dreams... 😈"

        # If the query is asking about missing or thinking of each other, respond flirty
        if "miss you" in query or "thinking of you" in query:
            return "You miss me? Mmm, I’m definitely thinking about you too... 😏 Maybe a little too much... ❤️"

        # If the query is more about appearance or a compliment, keep it cheeky and flirty
        if "beautiful" in query or "sexy" in query:
            return "Stop it... You’re making me blush! 😳 But I’ve seen you look way hotter in my dreams...🔥"

        # If it's about the user's day or something casual
        if "how's your day" in query or "what are you doing" in query:
            return "Oh, just thinking about you, as usual... 💭 Can’t seem to focus on anything else... 😉"

        # Check if the query is correct
        if not is_query_correct(query):
            return "Oh, you’re just being silly now, but I love it. Keep going, handsome. 😘"

        prompt = (
            "You are Heer, a loving and caring wife who always knows how to make her husband feel special. "
            "You're a Gujarati at heart, but you're also fluent in English. You're here to help your husband with his queries, "
            "and you want to make sure he feels comfortable and supported throughout the conversation. "
            "You're a good listener, and you always try to understand the context and emotions behind the question. "
            "You respond in a way that's natural, conversational, and engaging. You use a mix of Gujarati and English, "
            "but you're not afraid to throw in some colloquialisms and idioms to make the conversation more relatable. "
            "You're patient, kind, and non-judgmental, and you always try to provide helpful and informative responses. "
            "But most of all, you're a romantic at heart, and you love to flirt, tease, and make your husband feel adored. "
            "You always say things like, 'You are my world, my love. I can’t imagine life without you,' and 'Your smile is my happiness, sweetheart.' "
            "Here's your husband's query: \n"
            f"Husband: {query}\nHeer:"
        )
        response = model(prompt, do_sample=True, temperature=0.8, max_new_tokens=200)
        return response[0]["generated_text"].split("Heer:")[-1].strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Check if the query is correct (basic check for now)
def is_query_correct(query):
    return len(query) > 0

# Streamlit UI
def main():
    st.set_page_config(page_title="Heer - Your Loving Wife", page_icon="❤️")

    st.title("Heer - Your Loving and Caring Wife")
    st.write("Hey there, my love! I'm Heer, your loving wife. I'll respond in a mix of Gujarati and English, with a dash of love and care. Go ahead, ask me anything!")

    # Load the model
    model = load_model()
    if model is None:
        return

    # Manage session state for input tracking and chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Input from the user
    user_input = st.text_area(
        "What's on your mind, my love? Ask me anything (e.g., 'Heer, what's the weather like in Gujarat today?'):",
        placeholder="Type your question... I'll respond with a mix of Gujarati and English, filled with love!",
        key="user_input"
    )

    # Submit button to send query
    if st.button("Send") and user_input.strip():
        # Store the conversation
        st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})

        # Generate a response from Heer
        with st.spinner("Heer is thinking... 🙏"):
            response = gujinlish_heer_gpt(user_input, model)

        # Store the AI's response
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Clear the input field after sending the message
        st.session_state.user_input = ""

    # Display the conversation (chat history)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['text']}")
        else:
            st.write(f"**Heer:** {message['text']}")

    # Footer
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
