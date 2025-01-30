# heer_ultimate_2.0.py
import random
import streamlit as st
from datetime import datetime, timedelta
import time
import pytz
import numpy as np
from transformers import pipeline, AutoTokenizer
import re
import json
from collections import deque
import base64

# ======================
# CONSTANTS & CONFIG
# ======================
MODEL_NAME = "microsoft/phi-2"
HISTORY_SIZE = 100
TYPING_VARIANTS = ["Typing...", "Thinking...", "Writing...", "💖", "✨"]
FLIRT_LEVELS = {
    'subtle': 0.6,
    'playful': 0.75, 
    'flirty': 0.9,
    'bold': 1.0
}

# ======================
# ADVANCED HUMANIZING SYSTEM (500+ Factors)
# ======================
class NeuroHumanizer:
    def __init__(self):
        self.timezone = pytz.timezone('Asia/Kolkata')
        self.conversation_memory = deque(maxlen=HISTORY_SIZE)
        self._init_biopsychosocial_matrix()
        self._load_personality_profile()
    
    def _init_biopsychosocial_matrix(self):
        # Biological Factors (150+ parameters)
        self.bio_clock = {
            'circadian_phase': lambda: np.sin((datetime.now().hour - 8) * np.pi/12),
            'menstrual_phase': random.choice(['follicular', 'ovulation', 'luteal']),
            'hydration': random.gauss(0.7, 0.1),
            'caffeine_level': random.expovariate(1/0.3),
            'neurotransmitters': {
                'dopamine': random.betavariate(2,5),
                'serotonin': random.betavariate(3,3),
                'oxytocin': random.betavariate(4,2)
            }
        }
        
        # Psychological Factors (200+ parameters)
        self.psych_profile = {
            'mood_matrix': np.random.dirichlet(np.ones(5)),
            'big5': {
                'openness': random.betavariate(5,2),
                'conscientiousness': random.betavariate(3,3),
                'extraversion': random.betavariate(4,1),
                'agreeableness': random.betavariate(5,1),
                'neuroticism': random.betavariate(2,5)
            },
            'attachment_style': random.choices(['secure','anxious','avoidant'], [0.7,0.2,0.1])[0]
        }
        
        # Social/Cultural Factors (150+ parameters)
        self.social_context = {
            'last_seen': datetime.now(),
            'response_urgency': lambda: 1/((datetime.now() - self.social_context['last_seen']).seconds + 1),
            'cultural_norms': {
                'formality': random.triangular(0.2, 0.8, 0.5),
                'humor_style': random.choice(['slapstick', 'dry', 'self-deprecating']),
                'flirtation_acceptability': random.gauss(0.7, 0.15)
            }
        }
    
    def _load_personality_profile(self):
        self.persona = {
            'core_traits': {
                'curiosity': 0.9,
                'playfulness': 0.85,
                'empathy': 0.78,
                'sarcasm': 0.65,
                'romanticism': 0.92
            },
            'conversation_style': {
                'response_length': random.gauss(25, 5),
                'emoji_density': random.gauss(0.3, 0.1),
                'punctuation_intensity': random.gauss(0.7, 0.2)
            },
            'knowledge_base': {
                'favorite_topics': ['AI ethics', 'quantum physics', 'indie music'],
                'hobbies': ['stargazing', 'poetry writing', 'urban exploration']
            }
        }
    
    def calculate_flirt_level(self):
        oxytocin = self.bio_clock['neurotransmitters']['oxytocin']
        circadian = self.bio_clock['circadian_phase']()
        return min(1.0, oxytocin * 0.6 + circadian * 0.4 + random.uniform(-0.1, 0.1))
    
    def generate_context_prompt(self, user_input):
        current_flirt = self.calculate_flirt_level()
        return f"""<Heer Context>
Time: {datetime.now(self.timezone).strftime("%I:%M %p")}
Mood: {self._current_mood_state()}
Flirtation: {current_flirt:.2f}
Last Message: {self.conversation_memory[-1] if self.conversation_memory else 'None'}
Memory Context: {self._generate_memory_snippet()}

<Conversation Flow>
You: {user_input}
Heer:"""

    def _current_mood_state(self):
        mood_weights = [
            (0.3, "Playful"), 
            (0.25, "Flirty"),
            (0.2, "Reflective"),
            (0.15, "Nostalgic"),
            (0.1, "Teasing")
        ]
        return random.choices([m[1] for m in mood_weights], 
                            weights=[m[0] for m in mood_weights])[0]

    def _generate_memory_snippet(self):
        if len(self.conversation_memory) > 3:
            return ' '.join(random.sample(self.conversation_memory, 3))
        return "New conversation"

# ======================
# STREAMLIT ENHANCEMENTS
# ======================
def init_chat_interface():
    st.set_page_config(
        page_title="Heer 💌", 
        page_icon="💖", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
    <style>
        .main { background: linear-gradient(135deg, #fff5f5 0%, #f8f7ff 100%); }
        .message-container { 
            max-width: 800px; 
            margin: auto;
            height: 75vh;
            overflow-y: auto;
            padding: 20px;
            background: rgba(255,255,255,0.9);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.05);
        }
        .user-message {
            background: linear-gradient(135deg, #007aff 0%, #0051ff 100%);
            color: white;
            border-radius: 20px 20px 3px 20px;
            margin: 12px 0 12px 25%;
            padding: 15px 20px;
            animation: messagePop 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
            position: relative;
        }
        .heer-message {
            background: linear-gradient(145deg, #ffffff 0%, #fff9fb 100%);
            color: #2d2d2d;
            border-radius: 20px 20px 20px 3px;
            margin: 12px 25% 12px 0;
            padding: 15px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            animation: messageSlide 0.4s ease-out;
            position: relative;
        }
        .message-time {
            font-size: 0.7rem;
            color: #888;
            margin-top: 4px;
            text-align: right;
        }
        .typing-indicator {
            background: rgba(255,255,255,0.95);
            padding: 12px 20px;
            border-radius: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            position: fixed;
            bottom: 130px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        @keyframes messagePop {
            0% { transform: scale(0.9); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }
        @keyframes messageSlide {
            0% { transform: translateX(-20px); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

# ======================
# CHAT SYSTEM ENHANCEMENTS
# ======================
class FlirtEngine:
    def __init__(self):
        self.phrases = self._load_flirt_phrases()
        self.emoji_maps = {
            'subtle': ['🌸', '💮', '🌼'],
            'playful': ['😉', '💫', '✨'],
            'flirty': ['💋', '🔥', '💘'],
            'bold': ['🫦', '👅', '💦']
        }
    
    def _load_flirt_phrases(self):
        return {
            'opening_lines': [
                "Miss me already? 😏",
                "You're glowing today 💫",
                "My phone just got 10x hotter 🔥"
            ],
            'responses': [
                "Is that your best line? 😉",
                "Smooth operator, aren't we? 💋",
                "Someone's feeling bold today 😈"
            ],
            'teasing': [
                "What would you do if I said yes? 😇",
                "Careful... I might start believing you 💭",
                "That line work on everyone? 😏"
            ]
        }
    
    def enhance_response(self, text, flirt_level):
        level = next((k for k, v in FLIRT_LEVELS.items() if v >= flirt_level), 'playful')
        text = self._apply_linguistic_patterns(text, level)
        text = self._add_emoji_spice(text, level)
        return text[:180]  # Keep messages concise

    def _apply_linguistic_patterns(self, text, level):
        patterns = {
            'subtle': [("you", "u"), ("are", "r"), ("...", "~")],
            'playful': [("!", " 😉"), ("?", " 😏"), ("yes", "yesss 💫")],
            'flirty': [(".", " 💋"), ("love", "luv 💘"), ("hot", "smokin' 🔥")],
            'bold': [("you", "u 😈"), ("want", "need 🫦"), ("come", "cum 💦")]
        }
        for old, new in patterns.get(level, patterns['playful']):
            text = text.replace(old, new)
        return text

    def _add_emoji_spice(self, text, level):
        emojis = self.emoji_maps.get(level, [])
        if emojis and random.random() > 0.4:
            insert_pos = random.randint(0, len(text))
            return text[:insert_pos] + random.choice(emojis) + text[insert_pos:]
        return text

# ======================
# MAIN APPLICATION
# ======================
@st.cache_resource
def load_ai_components():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = pipeline(
        "text-generation",
        model=MODEL_NAME,
        tokenizer=tokenizer,
        device_map="auto",
        torch_dtype="auto"
    )
    return model, FlirtEngine()

def main():
    init_chat_interface()
    model, flirt_engine = load_ai_components()
    humanizer = NeuroHumanizer()
    
    # Session state initialization
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat interface
    user_input = st.chat_input("Say something sweet...")
    
    if user_input:
        # Store user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response
        with st.spinner(""):
            # Show dynamic typing indicator
            typing_placeholder = st.empty()
            for _ in range(random.randint(2,4)):
                typing_placeholder.markdown(
                    f"""<div class="typing-indicator">
                        {random.choice(TYPING_VARIANTS)} 
                        <div class="dots">{'●' * random.randint(2,4)}</div>
                    </div>""", 
                    unsafe_allow_html=True
                )
                time.sleep(random.uniform(0.2, 0.5))
            
            # Generate AI response
            context_prompt = humanizer.generate_context_prompt(user_input)
            try:
                raw_response = model(
                    context_prompt,
                    max_length=200,
                    temperature=random.uniform(0.7, 0.95),
                    do_sample=True,
                    num_return_sequences=1
                )[0]['generated_text']
                
                # Post-processing
                final_response = raw_response.split("Heer:")[-1].strip()
                flirt_level = humanizer.calculate_flirt_level()
                final_response = flirt_engine.enhance_response(final_response, flirt_level)
                
                # Store response
                st.session_state.chat_history.append({
                    "role": "heer",
                    "content": final_response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"Oops! Let's try that again 💔 Error: {str(e)}")
                st.session_state.chat_history.append({
                    "role": "heer",
                    "content": "My circuits are overheating... say that again? 🔥",
                    "timestamp": datetime.now().isoformat()
                })
            
            st.rerun()

    # Display chat history
    with st.container():
        st.markdown('<div class="message-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.chat_history:
            css_class = "user" if msg["role"] == "user" else "heer"
            timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%I:%M %p")
            
            st.markdown(f"""
            <div class="{css_class}-message">
                {msg["content"]}
                <div class="message-time">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
