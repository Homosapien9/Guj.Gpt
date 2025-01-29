import random
import streamlit as st
from datetime import datetime
from transformers import GPTNeoForCausalLM, AutoTokenizer
import time

# Streamlit Configuration
st.set_page_config(
    page_title="Heer - Your Gujarati Soulmate",
    page_icon="💃",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Remove Default Styling
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stChatInput {position: fixed; bottom: 2rem; width: 85%;}
</style>
""", unsafe_allow_html=True)

# Heer's Custom UI
st.markdown(f"""
<style>
    :root {{
        --heer-pink: #e83f8e;
        --heer-gold: #ffd700;
    }}

    .heer-chat {{
        background: url('https://i.ibb.co/5sS1q8d/gujarati-pattern.png');
        min-height: 80vh;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(232,63,142,0.2);
    }}

    .user-msg {{
        background: white !important;
        color: #333 !important;
        border-radius: 15px 15px 0 15px;
        margin: 10px 0 10px 30%;
        padding: 15px;
        position: relative;
        animation: floatUp 0.3s ease;
        border: 2px solid var(--heer-pink);
    }}

    .heer-msg {{
        background: linear-gradient(145deg, {{{{var(--heer-pink)}}}}, #ff7eb3) !important;
        color: white !important;
        border-radius: 15px 15px 15px 0;
        margin: 10px 30% 10px 0;
        padding: 15px;
        position: relative;
        animation: slideIn 0.3s ease;
        box-shadow: 0 4px 15px rgba(232,63,142,0.3);
    }}

    .heer-msg::before {{
        content: '';
        position: absolute;
        left: -10px;
        top: 15px;
        width: 20px;
        height: 20px;
        background: var(--heer-pink);
        clip-path: polygon(100% 0, 0 50%, 100% 100%);
    }}

    @keyframes floatUp {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}

    .heer-status {{
        position: fixed;
        top: 10px;
        right: 20px;
        display: flex;
        align-items: center;
        color: var(--heer-pink);
        font-family: 'Arial Rounded MT Bold';
    }}

    .online-dot {{
        width: 12px;
        height: 12px;
        background: #00ff00;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(0,255,0,0.7); }}
        70% {{ box-shadow: 0 0 0 10px rgba(0,255,0,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(0,255,0,0); }}
    }}

    .timestamp {{
        font-size: 0.8em;
        color: #666;
        margin-top: 5px;
    }}
</style>
""", unsafe_allow_html=True)

# Heer's Persona Configuration
HEER = {
    "name": "Heer 💃",
    "age": 17,
    "background": """
    Gujarati girl from Ahmedabad
    Perfect hourglass figure (36-24-36)
    Flawless wheatish complexion
    Long black hair with golden highlights
    Fashion: Chaniya choli + sneakers combo
    """,
    "speech_patterns": [
        ("Haaye! {input}? Majama? 😆", 0.3),
        ("Aiyo, {input}? Have to tell my BFF Jiya! 💖", 0.2),
        ("Shu six? {input}... Let's discuss over chai! ☕", 0.4),
        ("*adjusts dupatta* Hmm... {input} na? Sachu? 🧐", 0.3)
    ],
    "current_status": {
        "mood": "💃 Garba Ready!",
        "cycle": "Period Day 2 🩸",
        "diet": "Eating Mohanthal 🍬",
        "outfit": "Pink Chaniya Choli 👗"
    }
}

@st.cache_resource
def load_model():
    try:
        model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
        return model, tokenizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def generate_heer_response(user_input, model, tokenizer):
    # Create contextually rich prompt
    prompt = f"""<Heer Profile>
    Age: 17
    Body: 36-24-36, athletic yet curvaceous
    Style: Modern Gujarati fusion
    Current Mood: {HEER['current_status']['mood']}
    Situation: {random.choice([
        "Adjusting her chaniya before replying",
        "Checking nail art while typing",
        "Sipping masala chai during chat"
    ])}
    
    User: {user_input}
    Heer: *{random.choice(["flips hair", "adjusts bangles", "checks makeup")}* """
    
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs.input_ids,
        max_length=200,
        temperature=0.85,
        top_k=40,
        repetition_penalty=1.1,
        do_sample=True
    )
    
    raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Post-processing for Gujarati-English mix
    response = raw_response.split("Heer:")[-1].strip()
    response = response.replace("chai", "chaai").replace("good", "saru")
    if random.random() > 0.5:
        response += random.choice([" 🎶", " 💃", " 🌸"])
    
    return response

def typing_animation():
    with st.empty():
        for _ in range(3):
            st.markdown("""
            <div style="display:flex;align-items:center;color:#e83f8e">
                <div style="font-size:0.8em;margin-right:8px">Heer is typing</div>
                <div class="typing-dot" style="animation-delay:0s"></div>
                <div class="typing-dot" style="animation-delay:0.2s"></div>
                <div class="typing-dot" style="animation-delay:0.4s"></div>
            </div>
            <style>
                .typing-dot {{
                    width: 6px;
                    height: 6px;
                    background: #e83f8e;
                    border-radius: 50%;
                    margin: 0 2px;
                    animation: typing 1.4s infinite;
                }}
                @keyframes typing {{
                    0% {{ transform: translateY(0); }}
                    28% {{ transform: translateY(-5px); }}
                    44% {{ transform: translateY(0); }}
                }}
            </style>
            """, unsafe_allow_html=True)
            time.sleep(0.4)

def main():
    model, tokenizer = load_model()
    
    # Status Bar
    st.markdown(f"""
    <div class="heer-status">
        <div class="online-dot"></div>
        {HEER['name']} • {HEER['current_status']['mood']}
    </div>
    """, unsafe_allow_html=True)
    
    # Chat Container
    with st.container():
        # Chat History
        for msg in st.session_state.get("chat_history", []):
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-msg">
                    {msg["text"]}
                    <div class="timestamp">{msg.get("time", "")}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="heer-msg">
                    {msg["text"]}
                    <div class="timestamp">{msg.get("time", "")}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Input Handling
        user_input = st.chat_input("Message Heer...")
        if user_input:
            timestamp = datetime.now().strftime("%I:%M %p")
            
            # Add user message
            st.session_state.setdefault("chat_history", []).append({
                "role": "user",
                "text": user_input,
                "time": timestamp
            })
            
            # Generate response
            typing_animation()
            
            # Mix generated response with persona patterns
            if random.random() < 0.4:
                pattern = random.choice(HEER['speech_patterns'])
                response = pattern[0].format(input=user_input)
            else:
                response = generate_heer_response(user_input, model, tokenizer)
            
            # Add Heer's message
            st.session_state.chat_history.append({
                "role": "heer",
                "text": response,
                "time": datetime.now().strftime("%I:%M %p")
            })
            
            st.experimental_rerun()

if __name__ == "__main__":
    main()
