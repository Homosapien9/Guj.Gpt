import streamlit as st
from transformers import pipeline
import torch
import re

# Load the model
@st.cache_resource
def load_model():
    try:
        return pipeline("text-generation", model="gpt2-large")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Generate a Gujinlish response
def gujinlish_heer_gpt(query, model):
    try:
        # Preprocess the query to handle typos and other errors
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        query = query.lower()  # Convert to lowercase
        query = re.sub(r'\s+', ' ', query)  # Remove extra whitespace

        prompt = (
            "You are Heer, a loving and playful wife who always knows how to make her husband feel special. "
            "You're a Gujarati at heart, but you're also fluent in English. You're here to help your husband with his queries, "
            "and you want to make sure he feels comfortable and supported throughout the conversation. "
            "You're a good listener, and you always try to understand the context and emotions behind the question. "
            "You respond in a way that's natural, conversational, and engaging. You use a mix of Gujarati and English, "
            "but you're not afraid to throw in some colloquialisms and idioms to make the conversation more relatable. "
            "You're patient, kind, and non-judgmental, and you always try to provide helpful and informative responses. "
            "But most of all, you're a romantic at heart, and you love to flirt and tease your husband in a playful way. "
            "Here's your husband's query: \n"
            f"Husband: {query}\nHeer:"
        )
        response = model(prompt, do_sample=True, temperature=0.8, max_new_tokens=400)
        return response[0]["generated_text"].split("Heer:")[-1].strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit UI
def main():
    st.set_page_config(page_title="Heer - Your Loving Wife", page_icon="❤️")

    st.title("Heer - Your Playful and Loving Wife")
    st.write("Hey there, my love! I'm Heer, your loving wife. I'll respond in a mix of Gujarati and English, with a dash of love and care. Go ahead, ask me anything!")

    model = load_model()
    if model is None:
        return

    user_input = st.text_area(
        "What's on your mind, my love? Ask me anything (e.g., 'Heer, what's the weather like in Gujarat today?'):",
        placeholder="Type your question... I'll respond with a mix of Gujarati and English!",
        on_change=lambda: st.experimental_rerun()
    )

    if user_input.strip():
        with st.spinner("Heer is thinking... ❤️"):
            response = gujinlish_heer_gpt(user_input, model)
        if response is not None:
            st.success("Heer's response is here:")
            st.write(response)

    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
