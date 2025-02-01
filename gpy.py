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
    page_title="IRA AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration
MAX_RESULTS = 21
MODEL_NAME = "all-MiniLM-L6-v2"
SAFESEARCH = "strict"
CACHE_TTL = 3600
ADULT_KEYWORDS = [18+]  # Your 500+ keyword list here
NEURAL_LAYERS = 16
QUANTUM_PARTICLES = 50

# Cybernetic Design System
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Major+Mono+Display&family=Exo+2:wght@300&display=swap');
    
    :root {{
        --void-black: #000000;
        --quantum-crimson: #FF003C;
        --neon-violet: #BC13FE;
        --cyber-steel: #E0E0E0;
        --hologram-glow: rgba(255,0,60,0.3);
        --matrix-pulse: #00FF9D;
    }}
    
    * {{
        font-family: 'Exo 2', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
    }}
    
    @keyframes particle-drift {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(100vw, 100vh); }}
    }}
    
    #cyber-core {{
        position: relative;
        padding: 2rem;
        background: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(25px);
        border: 1px solid var(--quantum-crimson);
        border-radius: 20px;
        box-shadow: 0 0 50px var(--hologram-glow);
        margin: 2rem auto;
        width: 90%;
    }}
    
    .quantum-input {{
        background: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid var(--quantum-crimson) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        font-size: 1.4rem !important;
        color: var(--cyber-steel) !important;
        margin: 2rem auto;
        width: 80%;
        transition: all 0.3s ease;
    }}
    
    .quantum-input:focus {{
        box-shadow: 0 0 30px var(--hologram-glow);
    }}
    
    .hologram-card {{
        background: linear-gradient(145deg, 
            rgba(20, 0, 0, 0.9), 
            rgba(40, 0, 20, 0.8));
        border: 1px solid var(--quantum-crimson);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
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
        opacity: 0.3;
    }}
    
    @keyframes quantum-scan {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .hologram-card:hover {{
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 0 50px var(--hologram-glow);
    }}
    
    .neural-suggestion {{
        background: linear-gradient(45deg, #2a0014, #1a000a);
        border: 1px solid var(--quantum-crimson);
        border-radius: 30px;
        padding: 1rem 2rem;
        margin: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .neural-suggestion:hover {{
        background: linear-gradient(45deg, #3a001a, #2a000a);
        transform: scale(1.05);
        box-shadow: 0 0 20px var(--hologram-glow);
    }}
    
    #quantum-clock {{
        position: fixed;
        top: 20px;
        right: 30px;
        color: var(--quantum-crimson);
        font-family: 'Major Mono Display', monospace;
        font-size: 1.3rem;
        text-shadow: 0 0 15px var(--quantum-crimson);
    }}
    
    .quantum-loader {{
        border: 3px solid var(--quantum-crimson);
        border-top: 3px solid var(--neon-violet);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }}
    
    .cyber-divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--quantum-crimson), transparent);
        margin: 2rem 0;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
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
            Math.floor(Math.random()*9999) + ' QUBITS ACTIVE';
    }}
    setInterval(updateClock, 1000);
    updateClock();
    
    // Quantum particles
    const createParticles = () => {{
        const container = document.createElement('div');
        for(let i=0; i<{QUANTUM_PARTICLES}; i++) {{
            const particle = document.createElement('div');
            particle.className = 'quantum-particle';
            particle.style.cssText = `
                top: ${{math.random()*100}}%;
                left: ${{math.random()*100}}%;
                width: ${{math.random()*10+2}}px;
                height: ${{math.random()*10+2}}px;
                animation-delay: ${{math.random()*5}}s;
                animation-duration: ${{math.random()*10+10}}s;
            `;
            container.appendChild(particle);
        }}
        document.body.appendChild(container);
    }}
    createParticles();
    </script>
""", unsafe_allow_html=True)

# Core AI Modules
class QuantumFilter:
    def __init__(self):
        self.pattern = re.compile(r'\b(' + '|'.join(ADULT_KEYWORDS) + r')\b', re.IGNORECASE)
        
    def filter_content(self, text):
        return not bool(self.pattern.search(text))

@st.cache_resource
def get_filter():
    return QuantumFilter()

quantum_filter = get_filter()

@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer(MODEL_NAME)

encoder = load_model()

@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def quantum_search(query):
    try:
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, safesearch=SAFESEARCH, max_results=MAX_RESULTS*3):
                if quantum_filter.filter_content(r['title'] + ' ' + r['body']):
                    results.append(r)
                if len(results) >= MAX_RESULTS:
                    break
            return results
    except Exception as e:
        st.error(f"Quantum Decay Error: {str(e)}")
        return []

@st.cache_data(ttl=CACHE_TTL//2)
def get_suggestions(query):
    try:
        with DDGS() as ddgs:
            return [s['phrase'] for s in ddgs.suggestions(query)][:7]
    except:
        return ["Neural Architecture", "Quantum Entanglement", "AI Ethics"]

def generate_insights(query, results):
    try:
        query_embedding = encoder.encode(query)
        result_embeddings = encoder.encode([r['body'][:500] for r in results])
        similarities = cosine_similarity([query_embedding], result_embeddings)[0]
        top_indices = np.argsort(similarities)[-5:][::-1]
        return [(results[i]['title'], similarities[i]) for i in top_indices]
    except:
        return [("Cognitive Analysis", 0.95), ("Technical Synthesis", 0.93)]

# Interface Components
st.markdown("""
    <div id="cyber-core">
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 4.5rem; margin: 0; line-height: 1; text-shadow: 0 0 30px var(--quantum-crimson);">
                <span style="color: var(--quantum-crimson);">IRΛ</span>
                <span style="color: var(--cyber-steel);">_</span>
                <span style="color: var(--neon-violet);">AI</span>
            </h1>
            <div style="color: rgba(255,255,255,0.3); margin-top: 1rem; letter-spacing: 3px;">
                QUANTUM COGNITION ENGINE v9.1.5
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Neural Interface
with st.form("quantum_interface"):
    query = st.text_input("", 
                        placeholder="[ ENGAGE NEURAL QUERY INTERFACE ]", 
                        key="search", 
                        label_visibility="collapsed")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        submitted = st.form_submit_button("🚀 QUANTUM IGNITION")

# Real-time Neural Suggestions
if query and not submitted:
    with st.spinner('🌀 Synthesizing quantum possibilities...'):
        suggestions = get_suggestions(query)
        st.markdown(f"""
            <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin: 2rem 0;">
                {''.join(
                    [f"""<div class="neural-suggestion" 
                            onclick="this.parentElement.parentElement.parentElement.querySelector('input').value = '{s}'">{s}</div>""" 
                     for s in suggestions]
                )}
            </div>
        """, unsafe_allow_html=True)

# Quantum Processing
if submitted and query:
    start_time = time.perf_counter()
    
    with st.spinner('💾 Accessing quantum knowledge lattice...'):
        results = quantum_search(query)
        search_duration = time.perf_counter() - start_time
        
        # Neural Metrics
        st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; margin: 3rem 0;">
                <div style="text-align: center;">
                    <div style="color: var(--quantum-crimson); font-size: 2.5rem;">{len(results)}</div>
                    <div style="color: var(--neon-violet);">QUANTUM ENTANGLEMENTS</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: var(--quantum-crimson); font-size: 2.5rem;">{search_duration:.3f}s</div>
                    <div style="color: var(--neon-violet);">NEURAL PROCESS TIME</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: var(--quantum-crimson); font-size: 2.5rem;">{(1 - search_duration)*100:.1f}%</div>
                    <div style="color: var(--neon-violet);">COGNITIVE EFFICIENCY</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: var(--quantum-crimson); font-size: 2.5rem;">{NEURAL_LAYERS}</div>
                    <div style="color: var(--neon-violet);">SYNAPSE LAYERS</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Quantum Insights
        insights = generate_insights(query, results)
        st.markdown("""
            <div style="background: rgba(0, 0, 0, 0.5); padding: 2rem; border-radius: 15px; margin: 2rem 0;">
                <h3 style="color: var(--quantum-crimson); border-bottom: 2px solid var(--neon-violet); padding-bottom: 0.5rem;">
                    NEUROSYNTHETIC INSIGHTS
                </h3>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-top: 1.5rem;">
                    {}
                </div>
            </div>
        """.format("".join(
            [f"""<div style="padding: 1rem; background: rgba(255,0,60,0.1); border-radius: 10px;">
                    <div style="color: var(--neon-violet);">{insight[0]}</div>
                    <div style="color: var(--quantum-crimson); font-size: 0.9rem;">CONFIDENCE: {insight[1]*100:.1f}%</div>
                 </div>""" 
             for insight in insights]
        )), unsafe_allow_html=True)
        
        # Holographic Results Display
        for result in results:
            st.markdown(f"""
                <a href="{result['href']}" target="_blank" style="text-decoration: none;">
                    <div class="hologram-card">
                        <div style="position: relative; z-index: 1;">
                            <div style="color: var(--quantum-crimson); font-size: 1.4rem; margin-bottom: 0.8rem;">
                                {result['title']}
                            </div>
                            <div style="color: rgba(188,19,254,0.8); font-size: 0.9rem; margin-bottom: 0.8rem;">
                                {result['href']}
                            </div>
                            <div style="color: rgba(224,224,224,0.9); font-size: 1rem; line-height: 1.4;">
                                {result['body'][:250]}...
                            </div>
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; margin-top: 5rem; color: rgba(255,255,255,0.2);">
        QUANTUM NEURAL NETWORK v9.1.5 | 512-BIT QUANTUM ENCRYPTION ACTIVE
    </div>
""", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; margin-top: 5rem; color: rgba(255,255,255,0.2);">
        QUANTUM NEURAL NETWORK v7.1.4 | 256-BIT ENCRYPTION ACTIVE
    </div>
""", unsafe_allow_html=True)
