import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import torch
import asyncio
from concurrent.futures import ThreadPoolExecutor

# --------------------------
# QUANTUM INTERFACE ENGINE
# --------------------------
st.set_page_config(
    page_title="IRA AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'About': "⚡ DIGITAL COGNITION INTERFACE v9.8.2 ⚡"}
)

# --------------------------
# OPTIMIZED STYLING
# --------------------------
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Exo+2:wght@900&display=swap');
    
    :root {{
        --hologram-blue: #00f3ff;
        --plasma-purple: #8a2be2;
        --cyber-green: #00ff88;
        --neon-pink: #ff00ff;
        --depth-space: #000119;
    }}
    
    body {{
        background: var(--depth-space);
        overflow-x: hidden;
    }}
    
    .cyber-input {{
        background: rgba(0,0,0,0.3) !important;
        border: none !important;
        padding: 1.5rem 2rem !important;
        font-size: 1.5rem !important;
        color: var(--cyber-green) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }}
    
    .quantum-card {{
        background: linear-gradient(145deg, 
            rgba(16,16,26,0.95), 
            rgba(32,32,48,0.95)) !important;
        border: 1px solid rgba(138,43,226,0.5);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }}
    
    .neon-suggestion {{
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(138,43,226,0.1);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .cyber-header {{
        font-family: 'Orbitron', sans-serif !important;
        text-align: center;
        font-size: 3rem !important;
        background: linear-gradient(45deg, #00f3ff, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 2rem 0;
    }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# AI CORE SYSTEM
# --------------------------
@st.cache_resource
def load_cognitive_engine():
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        suggestion_base = [
            "Neural interface design patterns", "Quantum encryption methods",
            "Bio-digital convergence trends", "Metaverse economics",
            "AGI safety protocols", "Nanotech in medicine",
            "Dark matter propulsion systems", "Neuroplasticity enhancement",
            "Post-quantum cryptography", "Exoplanet colonization strategies"
        ]
        suggestion_embeddings = model.encode(suggestion_base)
        return model, suggestion_base, suggestion_embeddings
    except Exception as e:
        st.error(f"COGNITIVE ENGINE FAILURE: {str(e)}")
        return None, None, None

model, suggestions, suggestion_embeddings = load_cognitive_engine()

# --------------------------
# OPTIMIZED QUANTUM FUNCTIONS
# --------------------------
async def hyper_search(query):
    loop = asyncio.get_event_loop()
    try:
        with ThreadPoolExecutor() as executor:
            with DDGS() as ddgs:
                results = await loop.run_in_executor(
                    executor, 
                    lambda: list(ddgs.text(query, max_results=5))
                )
                return results[:5]  # Limit to 5 results
    except Exception as e:
        st.error(f"SEARCH QUANTUM DISRUPTION: {str(e)}")
        return []

@st.cache_data(ttl=300, show_spinner=False)
def neural_suggest(query):
    if model is None:
        return []
    query_embed = model.encode([query])
    sim_scores = cosine_similarity(query_embed, suggestion_embeddings)[0]
    return [suggestions[i] for i in np.argsort(sim_scores)[-3:][::-1]]

# --------------------------
# STREAMLIT INTERFACE
# --------------------------
def main():
    if model is None:
        st.error("COGNITIVE ENGINE FAILED TO INITIALIZE")
        return

    st.markdown("""
        <h1 class="cyber-header">
            HYPERION SEARCH
        </h1>
    """, unsafe_allow_html=True)
    
    query = st.text_input(" ", placeholder="▣ ENTER NEURAL QUERY VECTOR...", 
                         key="search", label_visibility="collapsed").strip()
    
    if query:
        with st.container():
            suggestions = neural_suggest(query)
            if suggestions:
                st.markdown("#### COGNITIVE PATTERN MATCHES")
                for sug in suggestions:
                    if st.button(sug, key=sug):
                        st.session_state.search = sug

        with st.spinner("SCANNING COSMIC DATABANKS..."):
            try:
                results = asyncio.run(hyper_search(query))
                
                if results:
                    query_embed = model.encode([query])
                    result_texts = [f"{r['title']} {r['body']}" for r in results]
                    result_embeddings = model.encode(result_texts, batch_size=16)
                    similarities = cosine_similarity(query_embed, result_embeddings)[0]
                    
                    st.markdown("#### QUANTUM ENTANGLEMENT RESULTS")
                    for i, result in enumerate(results):
                        with st.expander(f"{result['title']} (Coherence: {similarities[i]*100:.1f}%)"):
                            st.markdown(f"```\n{result['body']}\n```")
                else:
                    st.warning("ZERO MATCH FOUND IN QUANTUM FOAM")
            except Exception as e:
                st.error(f"QUANTUM FLUCTUATION DETECTED: {str(e)}")

if __name__ == "__main__":
    main()
