import streamlit as st
from duckduckgo_search import DDGS
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
import random

# Streamlit Config
st.set_page_config(
    page_title="IRA QNTM",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load SentenceTransformer model for auto-recommendation
model = SentenceTransformer('all-mpnet-base-v2')

# Default prompts to match with
DEFAULT_PROMPTS = [
    "Quantum Computing Trends", 
    "AI Ethics Framework", 
    "Neural Network Optimization", 
    "The Future of Artificial Intelligence", 
    "Quantum Entanglement and Communication"
]

# Function for getting the most similar prompts based on entered input
def get_similar_prompts(query, prompts):
    query_embedding = model.encode([query])
    prompt_embeddings = model.encode(prompts)
    similarities = cosine_similarity(query_embedding, prompt_embeddings)
    top_indices = np.argsort(similarities[0])[::-1]
    top_prompts = [prompts[i] for i in top_indices[:3]]
    return top_prompts

# Hyper-Modern Cybernetic Design System 7.0 with Floating Elements and Dynamic Particles
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Exo+2:wght@300&display=swap');
    
    :root {{
        --void-black: #000000;
        --quantum-crimson: #FF003C;
        --neon-violet: #BC13FE;
        --cyber-steel: #E0E0E0;
        --hologram-glow: rgba(255,0,60,0.3);
        --matrix-pulse: #00FF9D;
        --quantum-blue: #00f3ff;
        --cyber-light: rgba(255, 255, 255, 0.7);
        --neon-pink: #FF2B6D;
    }}
    
    * {{
        font-family: 'Exo 2', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        background: radial-gradient(ellipse at center, 
            #000000 0%, 
            #1a000a 60%, 
            #2a0014 100%);
        color: var(--cyber-steel);
        overflow-x: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
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
        0% {{
            transform: translate(0, 0);
        }}
        100% {{
            transform: translate(100vw, 100vh);
        }}
    }}
    
    .cyber-core {{
        position: relative;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(35px);
        border-radius: 20px;
        box-shadow: 0 0 80px var(--hologram-glow);
        width: 100%;
        max-width: 600px;
        transform-style: preserve-3d;
        animation: fadeInUp 1.5s ease-out;
        display: flex;
        flex-direction: column;
        align-items: center;
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
        background: rgba(0, 0, 0, 0.85) !important;
        border: none;
        border-radius: 20px;
        padding: 1.8rem !important;
        font-size: 2rem !important;
        color: var(--cyber-steel) !important;
        width: 100%;
        text-align: center;
        transition: all 0.4s ease;
        text-shadow: 0 0 15px var(--quantum-crimson);
        animation: pulse 1s infinite alternate;
        margin-bottom: 2rem;
        margin-top: 1rem;
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
        border: 2px solid var(--quantum-blue);
        outline: none;
    }}
    
    .quantum-button {{
        background: linear-gradient(145deg, var(--quantum-crimson), var(--neon-violet));
        color: var(--cyber-steel);
        border: none;
        padding: 1.5rem 3rem;
        font-size: 1.6rem;
        border-radius: 40px;
        cursor: pointer;
        margin-top: 2rem;
        box-shadow: 0 0 20px var(--quantum-blue);
        transition: 0.3s ease-in-out;
    }}
    
    .quantum-button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 30px var(--quantum-blue);
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
    
    </style>
""", unsafe_allow_html=True)

# UI components for the Streamlit app
st.markdown("# Welcome to IRA QNTM 🌌")
st.markdown("**Explore the quantum future with AI and technology.**")
st.markdown("Type a prompt, and auto-recommendations based on AI insights will be provided instantly.")

# User input
prompt = st.text_input("Enter a quantum or AI topic to explore:", value="", key="prompt_input", label_visibility="collapsed")

# Show entered text
if prompt:
    st.markdown(f"**You entered:** `{prompt}`")

    # Display a spinning loader while generating recommendations
    with st.spinner("Generating quantum insights... Please wait..."):
        time.sleep(1)

    # Get auto-recommendations using semantic similarity
    recommended_prompts = get_similar_prompts(prompt, DEFAULT_PROMPTS)
    st.markdown("### Quantum Recommendations:")
    
    for i, rec in enumerate(recommended_prompts):
        st.markdown(f"**{i + 1}. {rec}**")

# Add a "Generate Insights" button
if st.button("Generate Quantum Insights"):
    with st.spinner("Unlocking insights... Please wait..."):
        time.sleep(2)
    
    st.markdown("### Quantum Insights")
    insights = random.sample([
        "Quantum computing could make current encryption methods obsolete, pushing for new cryptographic algorithms.",
        "AI is on the brink of revolutionizing healthcare through quantum-enhanced machine learning models.",
        "In the next decade, quantum networks might enable unbreakable communication channels.",
    ], 3)
    
    for insight in insights:
        st.markdown(f"**💡 {insight}**")

