import streamlit as st
from duckduckgo_search import DDGS
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import datetime
import random
# Streamlit Config
st.set_page_config(
    page_title="QUANTUM AI",
    page_icon="💘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuration
MAX_RESULTS = 15
MODEL_NAME = "all-MiniLM-L6-v2"
SAFESEARCH = "strict"
CACHE_TTL = 1800

# Load AI Model
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer(MODEL_NAME)

encoder = load_model()

# Quantum Flirt CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Syne+Tactile&display=swap');
    
    :root {{
        --quantum-red: #ff0055;
        --cyber-black: #0a0a0a;
        --flirt-pink: #ff69b4;
        --hacker-glow: rgba(255,0,85,0.15);
    }}
    
    * {{
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    #quantum-clock {{
        position: fixed;
        top: 15px;
        right: 20px;
        color: var(--quantum-red);
        font-size: 1.2rem;
        text-shadow: 0 0 10px var(--flirt-pink);
        z-index: 999;
    }}
    
    .cyber-input {{
        background: rgba(10, 0, 0, 0.95) !important;
        border: 3px solid var(--quantum-red) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.4rem !important;
        color: var(--flirt-pink) !important;
        box-shadow: 0 0 40px var(--hacker-glow) !important;
        margin: 2rem auto;
        width: 80%;
    }}
    
    .result-card {{
        background: linear-gradient(145deg, 
            rgba(20, 0, 0, 0.95), 
            rgba(80, 0, 40, 0.85));
        border-left: 6px solid var(--flirt-pink);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .result-card:hover {{
        transform: translateX(10px);
        box-shadow: 0 0 30px var(--hacker-glow);
    }}
    
    .flirt-suggestion {{
        background: linear-gradient(45deg, var(--quantum-red), var(--flirt-pink));
        border-radius: 20px;
        padding: 0.5rem 1.2rem;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .flirt-suggestion:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 15px var(--flirt-pink);
    }}
    
    @media (max-width: 768px) {{
        .cyber-input {{ width: 95% !important; }}
        #quantum-clock {{ font-size: 1rem; right: 10px; }}
    }}
    
    <div id="quantum-clock"></div>
    <script>
    function updateClock() {{
        const options = {{ 
            timeZone: 'Asia/Kolkata',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false 
        }};
        document.getElementById('quantum-clock').innerHTML = 
            '🕒 ' + new Date().toLocaleTimeString('en-GB', options) + ' GMT';
    }}
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    </style>
""", unsafe_allow_html=True)

# Core Functions
@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def execute_search(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, safesearch=SAFESEARCH, max_results=MAX_RESULTS))
    except Exception as e:
        st.error(f"Quantum entanglement failed: {str(e)}")
        return []

@st.cache_data(ttl=CACHE_TTL//2)
def get_suggestions(query):
    try:
        with DDGS() as ddgs:
            base_suggestions = [s['phrase'] for s in ddgs.suggestions(query)]
            flirt_suggestions = ["Quantum Chemistry", "AI Romance", "Neural Attraction"]
            return (base_suggestions + flirt_suggestions)[:5]
    except:
        return ["Quantum Dating", "AI Love", "Digital Romance"]

def generate_recommendations(query, results):
    try:
        query_embedding = encoder.encode(query)
        result_embeddings = encoder.encode([r['body'][:200] for r in results])
        similarities = cosine_similarity([query_embedding], result_embeddings)[0]
        return [results[i]['title'] for i in np.argsort(similarities)[-3:][::-1]]
    except:
        return ["Quantum Compatibility", "AI Attraction", "Neural Chemistry"]

# UI Components
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; position: relative;'>
        <h1 style='font-size: 4rem; margin: 0;'>
            <span style='color: var(--quantum-red);'>QUANTUM</span>
            <span style='color: var(--flirt-pink);'>❤AI</span>
        </h1>
        <div style='color: rgba(255,255,255,0.3); margin-top: 1rem;'>
            Cognitive Romance Interface v3.1.4
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Interface
with st.form("quantum_flirt"):
    query = st.text_input("", 
                        placeholder="[ ENTER YOUR QUANTUM CRUSH ]", 
                        key="search", 
                        label_visibility="collapsed")
    
    col1, col2 = st.columns([5, 1])
    with col2:
        submitted = st.form_submit_button("💘 IGNITE SPARKS")

# Real-time Suggestions
if query and not submitted:
    with st.spinner('🔮 Calculating attraction vectors...'):
        suggestions = get_suggestions(query)
        st.markdown("""
            <div style='display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;'>
                {}
            </div>
        """.format("".join(
            [f"<div class='flirt-suggestion' onclick='this.parentElement.parentElement.parentElement.querySelector(\"input\").value = \"{s}\";'>{s}</div>" 
             for s in suggestions]
        )), unsafe_allow_html=True)

# Search Execution
if submitted and query:
    start_time = time.time()
    
    with st.spinner('💞 Entangling particles...'):
        results = execute_search(query)
        search_duration = time.time() - start_time
        
        # Metrics
        st.markdown(f"""
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0;'>
                <div style='text-align: center;'>
                    <div style='color: var(--flirt-pink); font-size: 2rem;'>{len(results)}</div>
                    <div style='color: var(--quantum-red);'>ENTANGLEMENTS</div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: var(--flirt-pink); font-size: 2rem;'>{search_duration:.2f}s</div>
                    <div style='color: var(--quantum-red);'>SPARK DURATION</div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: var(--flirt-pink); font-size: 2rem;'>{random.randint(85, 99)}%</div>
                    <div style='color: var(--quantum-red);'>CHEMISTRY</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Results
        for result in results:
            st.markdown(f"""
                <a href="{result['href']}" target="_blank" style="text-decoration: none;">
                    <div class='result-card'>
                        <div style='color: var(--flirt-pink); font-size: 1.3rem; margin-bottom: 0.5rem;'>
                            {result['title']}
                        </div>
                        <div style='color: rgba(255,105,180,0.8); font-size: 0.8rem; margin-bottom: 0.5rem;'>
                            {result['href']}
                        </div>
                        <div style='color: rgba(255,255,255,0.9); font-size: 0.9rem;'>
                            {result['body'][:150]}...
                        </div>
                    </div>
                </a>
            """, unsafe_allow_html=True)
    
    # Quantum Observability
    if st.secrets.get("OBSERVABILITY", False):
        from streamlit_observability import observability
        observability(log_level="INFO")
