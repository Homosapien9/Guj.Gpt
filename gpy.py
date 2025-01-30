# heer_supreme.py
import random
import streamlit as st
from datetime import datetime, timedelta
import time
import pytz
import numpy as np
from transformers import pipeline, AutoTokenizer
import torch
import re
import json
from collections import deque
from typing import Dict, List, Tuple, Optional
import base64
import sys

# ======================
# CONSTANTS & CONFIG
# ======================
MODEL_NAME = "microsoft/phi-2"
HISTORY_SIZE = 150
MAX_RESPONSE_LENGTH = 250
TYPING_VARIANTS = ["Typing...", "Thinking...", "Writing...", "💖", "✨"]
FLIRT_LEVELS = {'subtle': 0.6, 'playful': 0.75, 'flirty': 0.9, 'bold': 1.0}
TIMEZONE = pytz.timezone('Asia/Kolkata')

COLOR_PALETTE = {
    "background": "#0a0a0a",
    "primary_red": "#ff3860",
    "dark_bg": "#1a1a1a",
    "chat_bg": "#262626",
    "user_bubble": "#ff3860",
    "heer_bubble": "#333333",
    "text_primary": "#ffffff",
    "text_secondary": "#cccccc",
    "accent_red": "#ff1443",
    "typing_indicator": "#ff3860",
    "gradient_start": "#ff1443",
    "gradient_end": "#ff3860"
}

# ======================
# NEURO-HUMANIZER SYSTEM
# ======================
class NeuroHumanizer:
    def __init__(self):
        self.conversation_memory = deque(maxlen=HISTORY_SIZE)
        self._init_biopsychosocial_matrix()
        self._load_personality_profile()
    
    def _init_biopsychosocial_matrix(self):
        # Biological Parameters (150+)
        self.bio_clock = {
            'circadian_phase': lambda: np.sin((datetime.now().hour - 8) * np.pi/12),
            'hydration': random.gauss(0.7, 0.1),
            'neurotransmitters': {
                'dopamine': random.betavariate(2,5),
                'serotonin': random.betavariate(3,3),
                'oxytocin': random.betavariate(4,2)
            }
        }
        
        # Psychological Profile (200+)
        self.psych_profile = {
            'mood_matrix': np.random.dirichlet(np.ones(5)),
            'big5': {
                'openness': random.betavariate(5,2),
                'agreeableness': random.betavariate(5,1),
                'neuroticism': random.betavariate(2,5)
            },
            'attachment_style': random.choices(['secure','anxious','avoidant'], [0.7,0.2,0.1])[0]
        }
        
        # Social Context (150+)
        self.social_context = {
            'last_seen': datetime.now(),
            'cultural_norms': {
                'formality': random.triangular(0.2, 0.8, 0.5),
                'humor_style': random.choice(['slapstick', 'dry', 'self-deprecating'])
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
            }
        }
    
    def calculate_flirt_level(self):
        oxytocin = self.bio_clock['neurotransmitters']['oxytocin']
        circadian = self.bio_clock['circadian_phase']()
        return min(1.0, oxytocin * 0.6 + circadian * 0.4 + random.uniform(-0.1, 0.1))
    
    def generate_context_prompt(self, user_input: str) -> str:
        current_flirt = self.calculate_flirt_level()
        return f"""<Heer Context>
Time: {datetime.now(TIMEZONE).strftime("%I:%M %p")}
Mood: {self._current_mood_state()}
Flirtation: {current_flirt:.2f}
Memory Context: {self._generate_memory_snippet()}

<Conversation Flow>
You: {user_input}
Heer:"""

    def _current_mood_state(self) -> str:
        mood_weights = [
            (0.3, "Playful"), 
            (0.25, "Flirty"),
            (0.2, "Reflective"),
            (0.15, "Nostalgic"),
            (0.1, "Teasing")
        ]
        return random.choices([m[1] for m in mood_weights], 
                            weights=[m[0] for m in mood_weights])[0]

    def _generate_memory_snippet(self) -> str:
        if len(self.conversation_memory) > 3:
            return ' '.join(random.sample(self.conversation_memory, 3))
        return "New conversation"

# ======================
# FLIRT ENGINE
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
    
    def _load_flirt_phrases(self) -> Dict[str, List[str]]:
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
            ]
        }
    
    def enhance_response(self, text: str, flirt_level: float) -> str:
        level = next((k for k, v in FLIRT_LEVELS.items() if v >= flirt_level), 'playful')
        text = self._apply_linguistic_patterns(text, level)
        text = self._add_emoji_spice(text, level)
        return text[:MAX_RESPONSE_LENGTH]

    def _apply_linguistic_patterns(self, text: str, level: str) -> str:
        patterns = {
            'subtle': [("you", "u"), ("...", "~")],
            'playful': [("!", " 😉"), ("?", " 😏")],
            'flirty': [(".", " 💋"), ("love", "luv 💘")],
            'bold': [("you", "u 😈"), ("want", "need 🫦")]
        }
        for old, new in patterns.get(level, patterns['playful']):
            text = text.replace(old, new)
        return text

    def _add_emoji_spice(self, text: str, level: str) -> str:
        emojis = self.emoji_maps.get(level, [])
        if emojis and random.random() > 0.4:
            insert_pos = random.randint(0, len(text))
            return text[:insert_pos] + random.choice(emojis) + text[insert_pos:]
        return text

# ======================
# CHAT SYSTEM CORE
# ======================
class DarkChatSystem:
    def __init__(self):
        self.model = self._load_model()
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.chat_history = deque(maxlen=HISTORY_SIZE)
        self.humanizer = NeuroHumanizer()
        self.flirt_engine = FlirtEngine()
        self.typing_phrases = [
            "Decoding your heart...",
            "Calculating flirtation levels...",
            "Generating perfect response...",
            "Igniting passion circuits..."
        ]
        
    def _load_model(self):
        return pipeline(
            "text-generation",
            model=MODEL_NAME,
            tokenizer=self.tokenizer,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            low_cpu_mem_usage=True
        )
    
    def generate_response(self, user_input: str) -> str:
        """Generate response with dynamic context"""
        context_prompt = self.humanizer.generate_context_prompt(user_input)
        
        response = self.model(
            context_prompt,
            max_length=MAX_RESPONSE_LENGTH,
            temperature=random.uniform(0.7, 0.95),
            do_sample=True,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )[0]['generated_text']
        
        raw_response = response.split("Heer:")[-1].strip()
        flirt_level = self.humanizer.calculate_flirt_level()
        return self.flirt_engine.enhance_response(raw_response, flirt_level)

# ======================
# STREAMLIT UI ENGINE
# ======================
class UIManager:
    def __init__(self):
        self.typing_animations = ["●", "●●", "●●●"]
        self.last_update = time.time()
        
    def init_dark_theme(self):
        st.set_page_config(
            page_title="Heer Supreme 💋", 
            page_icon="🔥", 
            layout="centered",
            initial_sidebar_state="collapsed"
        )
        
        st.markdown(f"""
        <style>
            .main {{ background: {COLOR_PALETTE['background']}; }}
            .message-container {{
                background: {COLOR_PALETTE['chat_bg']};
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                height: 70vh;
                overflow-y: auto;
            }}
            .user-message {{
                background: linear-gradient(135deg, {COLOR_PALETTE['gradient_start']} 0%, {COLOR_PALETTE['gradient_end']} 100%);
                color: {COLOR_PALETTE['text_primary']};
                border-radius: 20px 20px 3px 20px;
                margin: 15px 0 15px 25%;
                padding: 15px 20px;
                animation: messagePop 0.4s cubic-bezier(0.18, 0.89, 0.32, 1.28);
                position: relative;
                border: 1px solid rgba(255,56,96,0.2);
            }}
            .heer-message {{
                background: {COLOR_PALETTE['heer_bubble']};
                color: {COLOR_PALETTE['text_primary']};
                border-radius: 20px 20px 20px 3px;
                margin: 15px 25% 15px 0;
                padding: 15px 20px;
                animation: messageSlide 0.4s ease-out;
                position: relative;
                border: 1px solid rgba(255,255,255,0.1);
            }}
            .typing-indicator {{
                background: {COLOR_PALETTE['dark_bg']};
                padding: 12px 20px;
                border-radius: 25px;
                position: fixed;
                bottom: 130px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                align-items: center;
                gap: 8px;
                border: 1px solid {COLOR_PALETTE['primary_red']};
                box-shadow: 0 4px 15px rgba(255,56,96,0.2);
            }}
            @keyframes messagePop {{
                0% {{ transform: scale(0.9); opacity: 0; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            @keyframes messageSlide {{
                0% {{ transform: translateX(-20px); opacity: 0; }}
                100% {{ transform: translateX(0); opacity: 1; }}
            }}
            .message-time {{
                font-size: 0.7rem;
                color: {COLOR_PALETTE['text_secondary']};
                margin-top: 4px;
                text-align: right;
            }}
            ::-webkit-scrollbar {{ width: 8px; }}
            ::-webkit-scrollbar-track {{ background: {COLOR_PALETTE['chat_bg']}; }}
            ::-webkit-scrollbar-thumb {{ background: {COLOR_PALETTE['primary_red']}; }}
        </style>
        """, unsafe_allow_html=True)

    def show_typing_indicator(self, placeholder):
        current_animation = self.typing_animations[int((time.time() % 1) * 3)]
        phrase = random.choice(DarkChatSystem().typing_phrases)
        
        placeholder.markdown(f"""
        <div class="typing-indicator">
            <span style="color: {COLOR_PALETTE['primary_red']}">{phrase}</span>
            <div style="display: flex; gap: 4px;">
                <span style="color: {COLOR_PALETTE['typing_indicator']}; 
                    animation: pulse 1s infinite">{current_animation[0]}</span>
                <span style="color: {COLOR_PALETTE['typing_indicator']}; 
                    animation: pulse 1s infinite 0.2s">{current_animation[1] if len(current_animation)>1 else ''}</span>
                <span style="color: {COLOR_PALETTE['typing_indicator']}; 
                    animation: pulse 1s infinite 0.4s">{current_animation[2] if len(current_animation)>2 else ''}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    def render_chat_history(self):
        with st.container():
            st.markdown('<div class="message-container">', unsafe_allow_html=True)
            
            for msg in st.session_state.chat_history:
                timestamp = datetime.fromisoformat(msg["timestamp"]).strftime("%I:%M %p")
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        {msg["content"]}
                        <div class="message-time">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="heer-message">
                        {msg["content"]}
                        <div class="message-time">{timestamp}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ======================
# MAIN APPLICATION
# ======================
@st.cache_resource
def load_chat_system():
    return DarkChatSystem()

def main():
    ui = UIManager()
    ui.init_dark_theme()
    chat_system = load_chat_system()
    
    # Initialize session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input
    user_input = st.chat_input("Your secret message...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response
        with st.spinner(""):
            typing_placeholder = st.empty()
            
            # Show typing animation
            start_time = time.time()
            while time.time() - start_time < random.uniform(0.8, 1.5):
                ui.show_typing_indicator(typing_placeholder)
                time.sleep(0.1)
            
            # Generate response
            try:
                response = chat_system.generate_response(user_input)
                
                st.session_state.chat_history.append({
                    "role": "heer",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                st.error(f"Passion system overload! 💔 {str(e)}")
                st.session_state.chat_history.append({
                    "role": "heer",
                    "content": "My circuits are overheating... say that again? 🔥",
                    "timestamp": datetime.now().isoformat()
                })
        
        st.rerun()
    
    # Render chat history
    ui.render_chat_history()

if __name__ == "__main__":
    main()
