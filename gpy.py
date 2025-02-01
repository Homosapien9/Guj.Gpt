import streamlit as st
from duckduckgo_search import DDGS
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
import random
import math

# Streamlit Config
st.set_page_config(
    page_title="IRA QNTM",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration
MAX_RESULTS = 21
MODEL_NAME = "all-mpnet-base-v2"  # More accurate model
SAFESEARCH = "strict"
CACHE_TTL = 3600
ADULT_KEYWORDS = [
    "18+", "xvideos", "pornhub", "adult", "explicit", "NSFW", 
    "sex", "porn", "erotic", "nude", "camgirl", "adultfilms", 
    "xxx", "fetish", "adultmovies", "sexvideos", "dirtytalk", 
    "hardcore", "submissive", "dominant", "stripper", 
    "xxxvideos", "sexchat", "pornstar", "swinger", "bdsm", "masturbation",
    "nudity", "hardcoreporn", "sexuallyexplicit", "shemale", "furry", 
    "incest", "lesbian", "gayporn", "hentai", "adulttoy", "sexshop",
    "threesome", "orgy", "webcamgirls", "toys", "fetishvideos", "roleplay",
    "sexuallycharged", "xxxstreaming", "pornhubpremium", "nsfwcontent", "adultwebsites"
]

NEURAL_LAYERS = 256
QUANTUM_PARTICLES = 100
DEFAULT_PROMPTS = ["Quantum Computing Trends", "AI Ethics Framework", "Neural Network Optimization"]

# Cybernetic Design System 2.0
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Major+Mono+Display&family=Exo+2:wght@300&family=Ubuntu+Mono&display=swap');
    
    :root {{
        --void-black: #000000;
        --quantum-crimson: #FF003C;
        --neon-violet: #BC13FE;
        --cyber-steel: #E0E0E0;
        --hologram-glow: rgba(255,0,60,0.3);
        --matrix-pulse: #00FF9D;
        --quantum-blue: #00f3ff;
    }}
    
    * {{
        font-family: 'Exo 2', sans-serif;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    body {{
        background: radial-gradient(ellipse at center, 
            #000000 0%, 
            #1a000a 60%, 
            #2a0014 100%);
        color: var(--cyber-steel);
        overflow-x: hidden;
    }}
    
    .quantum-particle {{
        position: fixed;
        pointer-events: none;
        background: radial-gradient(var(--quantum-crimson), transparent);
        opacity: 0.2;
        animation: particle-drift 20s linear infinite;
        z-index: -1;
    }}
    
    @keyframes particle-drift {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(100vw, 100vh); }}
    }}
    
    .cyber-core {{
        position: relative;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(35px);
        border: 1px solid var(--quantum-crimson);
        border-radius: 25px;
        box-shadow: 0 0 80px var(--hologram-glow);
        margin: 2rem auto;
        width: 90%;
        transform-style: preserve-3d;
    }}
    
    .quantum-input {{
        background: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid var(--quantum-crimson) !important;
        border-radius: 20px !important;
        padding: 1.8rem !important;
        font-size: 1.6rem !important;
        color: var(--cyber-steel) !important;
        margin: 3rem auto;
        width: 80%;
        transition: all 0.4s ease;
        text-shadow: 0 0 15px var(--quantum-crimson);
    }}
    
    .quantum-input:focus {{
        box-shadow: 0 0 50px var(--hologram-glow);
        border: 2px solid var(--quantum-blue) !important;
    }}
    
    .hologram-card {{
        background: linear-gradient(145deg, 
            rgba(20, 0, 0, 0.95), 
            rgba(40, 0, 20, 0.85));
        border: 1px solid var(--quantum-crimson);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        transform-style: preserve-3d;
    }}
    
    .hologram-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            var(--quantum-crimson),
            var(--neon-violet),
            transparent
        );
        animation: quantum-scan 8s linear infinite;
        opacity: 0.4;
    }}
    
    .hologram-card::after {{
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(120deg, 
            transparent 0%, 
            rgba(255,0,60,0.1) 50%, 
            transparent 100%);
        animation: hologram-pulse 4s infinite;
    }}
    
    @keyframes quantum-scan {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    @keyframes hologram-pulse {{
        0% {{ opacity: 0.2; }}
        50% {{ opacity: 0.4; }}
        100% {{ opacity: 0.2; }}
    }}
    
    .hologram-card:hover {{
        transform: translateY(-8px) rotateX(5deg) rotateY(5deg) scale(1.05);
        box-shadow: 0 0 80px var(--hologram-glow);
    }}
    
    .neural-suggestion {{
        background: linear-gradient(45deg, #2a0014, #1a000a);
        border: 1px solid var(--quantum-blue);
        border-radius: 30px;
        padding: 1.2rem 2.4rem;
        margin: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .neural-suggestion::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            var(--quantum-blue),
            transparent
        );
        animation: suggestion-glow 3s linear infinite;
    }}
    
    @keyframes suggestion-glow {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .neural-suggestion:hover {{
        transform: scale(1.08) rotate(2deg);
        box-shadow: 0 0 40px rgba(0, 243, 255, 0.3);
    }}
    
    .quantum-loader {{
        border: 4px solid var(--quantum-crimson);
        border-top: 4px solid var(--quantum-blue);
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }}
    
    .cyber-divider {{
        height: 3px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--quantum-crimson), 
            var(--quantum-blue), 
            transparent);
        margin: 3rem 0;
        animation: divider-pulse 3s ease infinite;
    }}
    
    @keyframes divider-pulse {{
        0% {{ opacity: 0.5; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.5; }}
    }}
    
    .quantum-metric {{
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid var(--quantum-blue);
        border-radius: 15px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    
    .quantum-metric::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(0, 243, 255, 0.1),
            transparent
        );
        animation: metric-scan 3s infinite;
    }}
    
    @keyframes metric-scan {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    </style>
    
    <div id="quantum-clock"></div>
    <script>
    function updateClock() {{
        const options = {{ 
            timeZone: 'UTC',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false 
        }};
        document.getElementById('quantum-clock').innerHTML = 
            '⏳ ' + new Date().toLocaleTimeString('en-US', options) + ' UTC | ' +
            Math.floor(Math.random()*9999) + ' QUBITS ENTANGLED';
    }}
    setInterval(updateClock, 1000);
    updateClock();
    
    // Quantum particles 2.0
    const createParticles = () => {{
        const container = document.createElement('div');
        for(let i=0; i<{QUANTUM_PARTICLES}; i++) {{
            const particle = document.createElement('div');
            particle.className = 'quantum-particle';
            particle.style.cssText = `
                top: ${{math.random()*120}}%;
                left: ${{math.random()*120}}%;
                width: ${{math.random()*15+5}}px;
                height: ${{math.random()*15+5}}px;
                animation-delay: ${{math.random()*10}}s;
                animation-duration: ${{math.random()*15+5}}s;
                filter: blur(${{math.random()*3+1}}px);
            `;
            container.appendChild(particle);
        }}
        document.body.appendChild(container);
    }}
    createParticles();
    
    // Quantum background effects
    document.body.addEventListener('mousemove', (e) => {{
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        document.documentElement.style.setProperty('--quantum-crimson', 
            `hsl(${{x * 360}}, 100%, 50%)`);
        document.documentElement.style.setProperty('--quantum-blue', 
            `hsl(${{y * 360}}, 100%, 50%)`);
    }});
    </script>
""", unsafe_allow_html=True)
