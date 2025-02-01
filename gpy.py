make it like waaaaaaaaaaaaay more futureistic with extreme tech and all like most interactive you can do and keepind in mind streamlit cloud parameter and making it best of all like best of best all things you can do to improve its gui do it with dark theme and seachbox should not be in box like make it beautiful and sexy and all other adjective you can addd make it 1000000000000x beautiful


import streamlit as st
from duckduckgo_search import DDGS
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

# Cybernetic Design System 2.0 with Animations
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
        animation: fadeInUp 1.5s ease-out;
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(50px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
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
        animation: pulse 1s infinite alternate;
    }}
    
    @keyframes pulse {{
        0% {{
            box-shadow: 0 0 10px var(--quantum-crimson);
        }}
        100% {{
            box-shadow: 0 0 25px var(--quantum-blue);
        }}
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
        animation: zoomIn 1s ease-out;
    }}
    
    @keyframes zoomIn {{
        0% {{
            transform: scale(0.8);
            opacity: 0;
        }}
        100% {{
            transform: scale(1);
            opacity: 1;
        }}
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
        animation: swing 2s ease-in-out infinite;
    }}
    
    @keyframes swing {{
        0% {{
            transform: rotate(0deg);
        }}
        50% {{
            transform: rotate(10deg);
        }}
        100% {{
            transform: rotate(0deg);
        }}
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
    
    @keyframes spin {{
        0% {{
            transform: rotate(0deg);
        }}
        100% {{
            transform: rotate(360deg);
        }}
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
""", unsafe_allow_html=True)

# UI components for the Streamlit app
st.markdown("# Welcome to IRA QNTM 🌌")
st.markdown("Explore the world of quantum computing and artificial intelligence.")
st.markdown("Enter a prompt and get insightful results.")

prompt = st.text_input("Enter your prompt here:", value=DEFAULT_PROMPTS[0], key="prompt_input")
if prompt:
    st.markdown(f"**You entered:** {prompt}")

# Button for generating quantum suggestions
if st.button("Generate Suggestions"):
    st.markdown("### Quantum Suggestions")
    st.markdown("These suggestions are based on the latest AI models.")

    suggestions = random.sample(DEFAULT_PROMPTS, 3)
    for suggestion in suggestions:
        st.markdown(f"**{suggestion}**")
