import streamlit as st
from transformers import pipeline, GPTNeoForCausalLM, AutoTokenizer
from datetime import datetime

# Set up Streamlit page config
st.set_page_config(page_title="Heer - Your Caring Girlfriend", page_icon="❤️", layout="wide")

# Load GPT-Neo 1.3B model and tokenizer
@st.cache_resource
def load_model():
    try:
        # Load GPT-Neo 1.3B model
        model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Helper function to determine time of day
def get_time_of_day():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "night"

# Function to generate a thoughtful, human-like response using GPT-Neo
def generate_chat_response(query, model, tokenizer):
    try:
        query = query.lower()
        
        # Add a greeting based on the time of day
        time_of_day = get_time_of_day()
        if time_of_day == "morning":
            greeting = "Good morning! How’s your day going so far?"
        elif time_of_day == "afternoon":
            greeting = "Hey! How’s your afternoon going? Anything exciting?"
        else:
            greeting = "Good night! Hope you had a nice day."

        # Prepare prompt and generate response
        input_text = f"{greeting} {query}"
        input_ids = tokenizer.encode(input_text, return_tensors="pt")

        # Generate a response from the model
        output = model.generate(input_ids, max_length=150, num_return_sequences=1, pad_token_id=50256)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Clean up the response to make it more human-like
        return response.replace(input_text, "").strip()

    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Streamlit user interface with improved chat bubbles
def main():
    # Set up the Streamlit page with custom styling
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
                animation: slideIn 0.5s ease-out;
            }
            .heer-msg {
                background-color: #4a4a4a;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 5px;
                align-self: flex-end;
                max-width: 75%;
                animation: slideIn 0.5s ease-out;
            }
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateX(20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
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

    # Load the GPT-Neo model and tokenizer
    model, tokenizer = load_model()
    if model is None or tokenizer is None:
        return

    # Manage session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display the conversation history with chat bubbles
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
            response = generate_chat_response(user_input, model, tokenizer)

        # Store the generated response
        if response:
            st.session_state.chat_history.append({"role": "heer", "text": response})

        # Manually clear the input field (without re-running the script)
        st.session_state.user_input = ""

    # Footer for the app
    st.write("---")
    st.write("Made with ❤️ by Jatan Shah")

if __name__ == "__main__":
    main()
