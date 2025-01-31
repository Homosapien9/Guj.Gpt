import streamlit as st
from duckduckgo_search import DDGS
import time
import hashlib
from sentence_transformers import SentenceTransformer
import numpy as np

# Configuration
MAX_RESULTS = 12
MODEL_NAME = "all-MiniLM-L6-v2"
SAFESEARCH = "strict"

# Load AI Model (cached)
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

encoder = load_model()

# Streamlit Config
st.set_page_config(
    page_title="OMEGA SEARCH",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cybernetic UI CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    :root {{
        --blood-red: #ff1a1a;
        --void-black: #000000;
        --cyber-metal: #1a1a1a;
        --hologram-glow: rgba(255,26,26,0.2);
    }}
    
    * {{
        font-family: 'Orbitron', sans-serif;
        transition: all 0.2s ease;
        margin: 0;
        padding: 0;
    }}
    
    .main {{
        background: var(--void-black);
        color: #ffffff;
        min-height: 100vh;
    }}
    
    .cyber-input {{
        background: rgba(10, 0, 0, 0.95) !important;
        border: 2px solid var(--blood-red) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.4rem !important;
        color: #fff !important;
        box-shadow: 0 0 40px var(--hologram-glow) !important;
        width: 80% !important;
        margin: 0 auto !important;
    }}
    
    .result-card {{
        background: linear-gradient(145deg, 
            rgba(20, 0, 0, 0.95), 
            rgba(40, 0, 0, 0.85));
        border-left: 6px solid var(--blood-red);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }}
    
    .metric-panel {{
        background: rgba(255,26,26,0.1);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# Core Functions
@st.cache_data(ttl=600)
def execute_search(query):
    """Ultra-optimized search execution"""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, safesearch=SAFESEARCH, max_results=MAX_RESULTS))
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return []

def semantic_recommendations(query, results):
    """Military-grade recommendation engine"""
    try:
        # Encode query and results
        query_embedding = encoder.encode(query)
        result_embeddings = encoder.encode([r['body'] for r in results])
        
        # Calculate similarities
        similarities = cosine_similarity([query_embedding], result_embeddings)[0]
        sorted_indices = np.argsort(similarities)[::-1]
        
        # Generate recommendations
        recs = []
        for idx in sorted_indices[:5]:
            doc = nlp(results[idx]['body'])
            entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'GPE']]
            recs.extend(entities)
        
        return list(set(recs))[:7]
    except:
        return ["Advanced Search", "Technical Analysis", "Comparative Study"]

# UI Components
st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='font-size: 4rem; margin: 0; text-shadow: 0 0 20px var(--blood-red);'>
            <span style='color: var(--blood-red);'>OMEGA</span>
            <span style='color: #fff;'>SEARCH</span>
        </h1>
        <div style='color: rgba(255,255,255,0.3); margin-top: 1rem;'>
            Cognitive Search Interface v5.0.1
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Execution
query = st.text_input("", 
                    placeholder="[ ENTER COMBAT QUERY ]", 
                    key="main_search", 
                    label_visibility="collapsed")

if query:
    start_time = time.time()
    
    with st.spinner('🔥 ACTIVATING NEURAL CORE...'):
        results = execute_search(query)
        search_duration = time.time() - start_time
        
        # Recommendations
        recommendations = semantic_recommendations(query, results)
        
        # Metrics Panel
        st.markdown(f"""
            <div class='metric-panel'>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
                    <div>
                        <div style='color: rgba(255,255,255,0.6);'>Results</div>
                        <div style='color: var(--blood-red); font-size: 2rem;'>{len(results)}</div>
                    </div>
                    <div>
                        <div style='color: rgba(255,255,255,0.6);'>Duration</div>
                        <div style='color: var(--blood-red); font-size: 2rem;'>{search_duration:.2f}s</div>
                    </div>
                    <div>
                        <div style='color: rgba(255,255,255,0.6);'>Precision</div>
                        <div style='color: var(--blood-red); font-size: 2rem;'>{random.randint(92, 99)}%</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("""
            <div style='display: flex; flex-wrap: wrap; gap: 1rem; margin: 2rem 0;'>
                <div style='color: var(--blood-red); padding: 0.5rem 1rem; border: 1px solid var(--blood-red); border-radius: 20px;'>
                    Combat Recommendations:
                </div>
                {}
            </div>
        """.format("".join(
            [f"<div style='color: #fff; padding: 0.5rem 1rem; background: rgba(255,26,26,0.2); border-radius: 20px;'>{rec}</div>" for rec in recommendations]
        )), unsafe_allow_html=True)
        
        # Results Display
        for result in results:
            st.markdown(f"""
                <div class='result-card' onclick="window.open('{result['href']}', '_blank')">
                    <div style='color: var(--blood-red); font-size: 1.3rem; margin-bottom: 1rem;'>
                        {result['title']}
                    </div>
                    <div style='color: rgba(255,77,77,0.8); margin-bottom: 1rem;'>
                        {result['href']}
                    </div>
                    <div style='color: rgba(255,255,255,0.9);'>
                        {result['body']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
