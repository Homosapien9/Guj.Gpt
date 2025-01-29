import random
import streamlit as st
from datetime import datetime
import time
from transformers import GPTNeoForCausalLM, AutoTokenizer

# Streamlit Configuration
st.set_page_config(
    page_title="Heer - Your Perfect Partner",
    page_icon="💘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Optimized UI Design
st.markdown("""
<style>
    :root {
        --passion: #ff2d55;
        --intimacy: #ff6b6b;
        --text: #2e2e2e;
    }

    .chat-container {
        background: linear-gradient(135deg, #fff5f7 0%, #fff0f7 100%);
        min-height: 85vh;
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(255,45,85,0.1);
    }

    .user-msg {
        background: var(--passion) !important;
        color: white !important;
        border-radius: 25px 4px 25px 25px;
        margin: 15px 0 15px 25%;
        padding: 15px 20px;
        animation: floatUp 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        backdrop-filter: blur(5px);
    }

    .heer-msg {
        background: linear-gradient(135deg, var(--intimacy), #ff8e8e) !important;
        color: white !important;
        border-radius: 4px 25px 25px 25px;
        margin: 15px 25% 15px 0;
        padding: 15px 20px;
        animation: slideIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        backdrop-filter: blur(5px);
    }

    .timestamp {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 5px;
    }

    @keyframes floatUp {
        from { transform: translateY(20px) scale(0.95); opacity: 0; }
        to { transform: translateY(0) scale(1); opacity: 1; }
    }

    .typing-indicator {
        display: inline-flex;
        align-items: center;
        padding: 8px 15px;
        background: rgba(255,255,255,0.9);
        border-radius: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Persona Configuration
HEER_PROFILE = {
    "name": "Heer 💘",
    "age": 17,
    "traits": {
        "physical": "5'4\", hourglass figure, radiant wheatish skin",
        "style": "Modern chaniya-choli with sneakers",
        "personality": ["Affectionate", "Playful", "Emotionally Intelligent"]
    },
    "relationship": {
        "status": "Committed since 8 months",
        "petnames": ["Jaanu", "Love", "Habibi"],
        "memories": {
            "first_kiss": "At Chowpatty Beach during sunset",
            "anniversary": "October 12th"
        }
    },
    "response_patterns": [
        ("*giggles* {input}? You're being naughty again! 😏", 0.4),
        ("*bites lip* Remember when we {memory}... 😳", 0.3),
        ("*leans closer* Why don't you {suggestion}? 💋", 0.5)
    ]
}

@st.cache_resource
def load_model():
    model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

def generate_intimate_response(user_input, model, tokenizer):
    # Optimized prompt template
    prompt = f"""<Heer's Mind>
Personality: {HEER_PROFILE['traits']['personality'][0]}, {random.choice(HEER_PROFILE['traits']['personality'])}
Current Mood: {random.choice(["Playful", "Loving", "Teasing"])}
Relationship Status: {HEER_PROFILE['relationship']['status']}
Physical State: {random.choice(["Adjusting dupatta", "Twirling hair", "Applying lip balm"])}

<Conversation>
You ({HEER_PROFILE['relationship']['petnames'][0]}): {user_input}
Heer: *{random.choice(["smirks", "blushes", "whispers"])}* """

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    
    outputs = model.generate(
        inputs.input_ids,
        max_length=150,
        temperature=0.9,
        top_p=0.92,
        repetition_penalty=1.15,
        do_sample=True
    )
    
    raw_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = raw_response.split("Heer:")[-1].strip()
    
    # Post-processing
    response = response.replace("?", "~").replace(".", "!")[:120]  # Keep responses concise
    if random.random() < 0.6:
        response += random.choice([" 💋", " ✨", " 😘"])
    
    return response

def main():
    model, tokenizer = load_model()
    
    # Session State Management
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat Interface
    with st.container():
        # Header
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:2rem">
            <h1 style="color:var(--passion); font-family:'Arial Rounded MT Bold'">{HEER_PROFILE['name']}</h1>
            <p style="color:var(--text)">{HEER_PROFILE['traits']['physical']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat History
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-msg">
                    {msg["text"]}
                    <div class="timestamp">{msg["time"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="heer-msg">
                    {msg["text"]}
                    <div class="timestamp">{msg["time"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Input Handling
        user_input = st.chat_input("Message Heer...")
        if user_input:
            # Store user message
            st.session_state.chat_history.append({
                "role": "user",
                "text": user_input,
                "time": datetime.now().strftime("%I:%M %p")
            })
            
            # Generate response with typing indicator
            with st.spinner(""):
                with st.empty():
                    st.markdown("""
                    <div class="typing-indicator">
                        <div style="margin-right:8px">Heer is typing</div>
                        <div style="display:flex;gap:3px">
                            <div style="width:6px;height:6px;background:var(--passion);border-radius:50%;animation: bounce 1s infinite"></div>
                            <div style="width:6px;height:6px;background:var(--passion);border-radius:50%;animation: bounce 1s infinite 0.2s"></div>
                            <div style="width:6px;height:6px;background:var(--passion);border-radius:50%;animation: bounce 1s infinite 0.4s"></div>
                        </div>
                    </div>
                    <style>
                        @keyframes bounce {
                            0%, 100% { transform: translateY(0); }
                            50% { transform: translateY(-3px); }
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    time.sleep(random.uniform(0.8, 1.5))  # Realistic typing delay
                
                # Generate response
                response = generate_intimate_response(user_input, model, tokenizer)
                
                # Store Heer's response
                st.session_state.chat_history.append({
                    "role": "heer",
                    "text": response,
                    "time": datetime.now().strftime("%I:%M %p")
                })
                
                st.rerun()

if __name__ == "__main__":
    main()
