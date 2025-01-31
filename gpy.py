# requirements.txt
# duckduckgo-search==3.9.4
# streamlit==1.29.0
# sentence-transformers==2.2.2
# scikit-learn==1.2.2
# numpy==1.24.3

import streamlit as st
from duckduckgo_search import DDGS
import time
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Streamlit Config
st.set_page_config(
    page_title="QUANTUMAI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration
MAX_RESULTS = 12
MODEL_NAME = "all-MiniLM-L6-v2"
SAFESEARCH = "strict"
CACHE_TTL = 3600  # 1 hour

# Load AI Model (cached)
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer(MODEL_NAME)

encoder = load_model()

# Quantum UI CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Audiowide&display=swap');
    
    :root {{
        --quantum-blue: #00f3ff;
        --neon-purple: #bc13fe;
        --void-black: #000000;
        --hologram-glow: rgba(0, 243, 255, 0.2);
    }}
    
    * {{
        font-family: 'Audiowide', sans-serif;
        margin: 0;
        padding: 0;
    }}
    
    .main {{
        background: radial-gradient(circle at center, #000428 0%, #004e92 150%);
        min-height: 100vh;
    }}
    
    .quantum-input {{
        background: rgba(0, 10, 30, 0.95) !important;
        border: 2px solid var(--quantum-blue) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        font-size: 1.2rem !important;
        color: var(--quantum-blue) !important;
        box-shadow: 0 0 50px var(--hologram-glow) !important;
        width: 80% !important;
        margin: 0 auto !important;
    }}
    
    .result-card {{
        background: linear-gradient(145deg, 
            rgba(0, 20, 40, 0.95), 
            rgba(0, 50, 100, 0.85));
        border-left: 6px solid var(--quantum-blue);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(5px);
        cursor: pointer;
        transition: transform 0.2s ease;
    }}
    
    .result-card:hover {{
        transform: translateX(10px);
        box-shadow: 0 0 20px var(--hologram-glow);
    }}
    
    .metric-panel {{
        background: rgba(0, 243, 255, 0.1);
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }}
    
    @media (max-width: 768px) {{
        .quantum-input {{
            width: 95% !important;
            padding: 1rem !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# Core Functions
@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def execute_search(query):
    """Optimized quantum search execution"""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, safesearch=SAFESEARCH, max_results=MAX_RESULTS))
    except Exception as e:
        st.error(f"Quantum flux disturbance: {str(e)}")
        return []

@st.cache_data(ttl=CACHE_TTL//2)
def get_suggestions(query):
    """Cached quantum suggestions"""
    try:
        with DDGS() as ddgs:
            return [s['phrase'] for s in ddgs.suggestions(query)][:5]
    except:
        return ["Quantum Computing", "AI Ethics", "Neural Networks"]

def generate_recommendations(query, results):
    """Optimized recommendation engine"""
    try:
        query_embedding = encoder.encode(query)
        result_embeddings = encoder.encode([r['body'][:200] for r in results])  # Truncate for speed
        similarities = cosine_similarity([query_embedding], result_embeddings)[0]
        return [results[i]['title'] for i in np.argsort(similarities)[-3:][::-1]]
    except:
        return ["Advanced Search", "Technical Analysis", "Comparative Study"]

# UI Components
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin: 0; text-shadow: 0 0 20px var(--quantum-blue);'>
            <span style='color: var(--quantum-blue);'>QUANTUM</span>
            <span style='color: var(--neon-purple);'>AI</span>
        </h1>
        <div style='color: rgba(255,255,255,0.3); margin-top: 0.5rem;'>
            Quantum Cognitive Interface v2.3.1
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Interface
with st.form("quantum_search"):
    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input("", 
                            placeholder="[ ENTER QUANTUM QUERY ]", 
                            key="search", 
                            label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("🌌 SEARCH")

# Real-time Suggestions
if query and not submitted:
    with st.spinner('🌀 Entangling quantum states...'):
        suggestions = get_suggestions(query)
        st.markdown("""
            <div style='display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;'>
                <div style='color: var(--quantum-blue); padding: 0.3rem 0.8rem; border: 1px solid var(--quantum-blue); border-radius: 15px;'>
                    Suggestions:
                </div>
                {}
            </div>
        """.format("".join(
            [f"<div style='color: #fff; padding: 0.3rem 0.8rem; background: rgba(0, 243, 255, 0.2); border-radius: 15px;'>{s}</div>" 
             for s in suggestions]
        )), unsafe_allow_html=True)

# Search Execution
if submitted and query:
    start_time = time.time()
    
    with st.spinner('⚛️ Collapsing quantum probabilities...'):
        results = execute_search(query)
        search_duration = time.time() - start_time
        
        # Metrics
        st.markdown(f"""
            <div class='metric-panel'>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;'>
                    <div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>Qubits</div>
                        <div style='color: var(--quantum-blue); font-size: 1.5rem;'>{len(results)}</div>
                    </div>
                    <div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>Duration</div>
                        <div style='color: var(--quantum-blue); font-size: 1.5rem;'>{search_duration:.2f}s</div>
                    </div>
                    <div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>Certainty</div>
                        <div style='color: var(--quantum-blue); font-size: 1.5rem;'>{min(99, int(95 - (search_duration*10)))}%</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        recommendations = generate_recommendations(query, results)
        st.markdown("""
            <div style='display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;'>
                <div style='color: var(--neon-purple); padding: 0.3rem 0.8rem; border: 1px solid var(--neon-purple); border-radius: 15px;'>
                    Recommendations:
                </div>
                {}
            </div>
        """.format("".join(
            [f"<div style='color: #fff; padding: 0.3rem 0.8rem; background: rgba(188, 19, 254, 0.2); border-radius: 15px;'>{r[:25]}</div>" 
             for r in recommendations]
        )), unsafe_allow_html=True)
        
        # Results
        for result in results:
            st.markdown(f"""
                <a href="{result['href']}" target="_blank" style="text-decoration: none;">
                    <div class='result-card'>
                        <div style='color: var(--quantum-blue); font-size: 1.1rem; margin-bottom: 0.5rem;'>
                            {result['title']}
                        </div>
                        <div style='color: rgba(0, 243, 255, 0.8); font-size: 0.8rem; margin-bottom: 0.5rem;'>
                            {result['href']}
                        </div>
                        <div style='color: rgba(255,255,255,0.9); font-size: 0.9rem;'>
                            {result['body'][:150]}...
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)
