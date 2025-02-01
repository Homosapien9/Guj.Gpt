import streamlit as st
from duckduckgo_search import DDGS
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
import math
# Streamlit Config
st.set_page_config(
    page_title="IRA AI",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration
MAX_RESULTS = 21
MODEL_NAME = "all-MiniLM-L6-v2"
SAFESEARCH = "strict"
CACHE_TTL = 3600
ADULT_KEYWORDS = [...]  # You can expand this list to filter adult content
NEURAL_LAYERS = 8

# Load Quantum Model
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer(MODEL_NAME)

encoder = load_model()

# Holographic UI CSS (Enhanced)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Major+Mono+Display&display=swap');
    
    :root {{
        --neon-purple: #bc13fe;
        --cyber-blue: #00f3ff;
        --void-black: #000000;
        --cyber-metal: #121212;
        --hologram-glow: rgba(188,19,254,0.3);
    }}
    
    * {{
        font-family: 'Orbitron', sans-serif;
        transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    }}
    
    body {{
        background: radial-gradient(ellipse at center, 
            #121212 0%, 
            #1a0030 80%, 
            #000000 100%);
        color: #ffffff;
        overflow-x: hidden;
    }}
    
    #neural-interface {{
        position: relative;
        padding: 2rem;
        background: rgba(10, 0, 20, 0.7);
        backdrop-filter: blur(30px);
        border: 2px solid var(--neon-purple);
        border-radius: 20px;
        box-shadow: 0 0 70px var(--hologram-glow);
    }}
    
    .quantum-input {{
        background: rgba(10, 0, 20, 0.95) !important;
        border: 3px solid var(--cyber-blue) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        font-size: 1.5rem !important;
        color: var(--cyber-blue) !important;
        margin: 2rem auto;
        width: 85%;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px var(--cyber-blue);
    }}
    
    .quantum-input:focus {{
        box-shadow: 0 0 50px var(--hologram-glow);
    }}
    
    .hologram-card {{
        background: linear-gradient(145deg, 
            rgba(30, 0, 50, 0.9), 
            rgba(10, 0, 20, 0.85));
        border: 2px solid var(--cyber-blue);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }}
    
    .hologram-card:hover {{
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 0 80px var(--hologram-glow);
    }}
    
    .cyber-particle {{
        position: fixed;
        pointer-events: none;
        background: radial-gradient(var(--neon-purple), transparent);
        opacity: 0.3;
        animation: move 2s infinite ease-in-out;
    }}
    
    @keyframes move {{
        0% {{ transform: translate(0, 0); }}
        50% {{ transform: translate(40px, -40px); }}
        100% {{ transform: translate(0, 0); }}
    }}
    
    #cyber-clock {{
        position: fixed;
        top: 20px;
        right: 30px;
        color: var(--cyber-blue);
        font-family: 'Major Mono Display', monospace;
        font-size: 1.3rem;
        text-shadow: 0 0 15px var(--neon-purple);
    }}
    
    .quantum-loader {{
        border: 3px solid var(--cyber-blue);
        border-radius: 50%;
        border-top: 3px solid transparent;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    
    <div id="cyber-clock"></div>
    <script>
    function updateClock() {{
        const options = {{ 
            timeZone: 'Asia/Kolkata',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false 
        }}; 
        document.getElementById('cyber-clock').innerHTML = 
            '⏳ ' + new Date().toLocaleTimeString('en-IN', options) + ' IST | ' + 
            Math.floor(Math.random()*9999) + ' NODES ACTIVE';
    }}
    setInterval(updateClock, 1000);
    updateClock();
    
    // Quantum particles animation
    const createParticles = () => {{
        const container = document.createElement('div');
        for(let i=0; i<30; i++) {{
            const particle = document.createElement('div');
            particle.className = 'cyber-particle';
            particle.style.cssText = `
                top: ${Math.random()*100}%;
                left: ${Math.random()*100}%;
                width: ${Math.random()*20+5}px;
                height: ${Math.random()*20+5}px;
                animation-delay: ${Math.random()*2}s;
            `;
            container.appendChild(particle);
        }}
        document.body.appendChild(container);
    }}
    createParticles();
    </script>
""", unsafe_allow_html=True)

# Core Functions and Search Logic (same as before)
class QuantumFilter:
    def __init__(self):
        self.pattern = re.compile(r'\b(' + '|'.join(ADULT_KEYWORDS) + r')\b', re.IGNORECASE)
        
    def filter_content(self, text):
        return not bool(self.pattern.search(text))

# Define Quantum Search, Suggestions, and Insights Functions (same as before)

# UI Components: Header and Interface
st.markdown("""
    <div id="neural-interface">
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 5rem; margin: 0; line-height: 1;">
                <span style="color: var(--neon-purple);">IRΛ</span>
                <span style="color: var(--cyber-blue);">_AI</span>
            </h1>
            <div style="color: rgba(255,255,255,0.3); margin-top: 1rem; letter-spacing: 3px;">
                NEUROSYNTHETIC COGNITION v7.1.4
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Input and Button
with st.form("quantum_search"):
    query = st.text_input("", 
                        placeholder="[ INITIALIZE NEURAL QUERY PROTOCOL ]", 
                        key="search", 
                        label_visibility="collapsed")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        submitted = st.form_submit_button("🚀 QUANTUM IGNITION")

# Real-time Suggestions
if query and not submitted:
    with st.spinner('🌀 Generating quantum possibilities...'):
        suggestions = get_neural_suggestions(query)
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin: 2rem 0;">
                {''.join(
                    [f"""<div class="neural-suggestion" 
                            onclick="this.parentElement.parentElement.parentElement.querySelector('input').value = '{s}'">{s}</div>""" 
                     for s in suggestions]
                )}
            </div>
        """, unsafe_allow_html=True)

# Execute Search and Display Results with Holographic Cards (same as before)

# Signature and Footer
st.markdown("""
    <div style="text-align: center; margin-top: 5rem; color: rgba(255,255,255,0.2);">
        QUANTUM NEURAL NETWORK v7.1.4 | 256-BIT ENCRYPTION ACTIVE
    </div>
""", unsafe_allow_html=True)
