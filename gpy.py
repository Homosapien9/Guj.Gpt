import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import asyncio
from concurrent.futures import ThreadPoolExecutor

# --------------------------
# QUANTUM CORE INIT
# --------------------------
st.set_page_config(
    page_title="IRA AI",
    page_icon="🌀",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={'About': "🌀 HOLOGRAPHIC COGNITION INTERFACE v13.0"}
)

# --------------------------
# NEURAL INTERFACE STYLING
# --------------------------
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Syne+Mono&family=Major+Mono+Display&display=swap');
    
    :root {{
        --void-black: #0a0a12;
        --neon-red: #ff0044;
        --hologram-pink: #ff00ff;
        --cyber-orange: #ff6600;
        --quantum-gradient: radial-gradient(circle at 50% 50%, #180028, #000000);
        --glow-intensity: 1;
    }}
    
    body {{
        background: var(--quantum-gradient);
        font-family: 'Syne Mono', monospace;
        color: #fff;
        overflow-x: hidden;
        margin: 0;
        padding: 0;
    }}
    
    /* Neural Input Field */
    .stTextInput>div>div>input {{
        background: rgba(0,0,0,0.2) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1.5rem 2rem !important;
        font-size: 1.5rem !important;
        color: var(--neon-red) !important;
        box-shadow: 0 0 50px rgba(255,0,68,0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px);
    }}
    
    .stTextInput>div>div>input:focus {{
        box-shadow: 0 0 80px rgba(255,0,68,0.5) !important;
        background: rgba(0,0,0,0.4) !important;
    }}
    
    /* Dynamic Content Flow */
    .quantum-response {{
        position: relative;
        padding: 2rem;
        margin: 2rem 0;
        background: linear-gradient(145deg, rgba(18,0,31,0.4), rgba(10,10,18,0.4));
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255,0,68,0.3);
        transition: all 0.4s ease;
        opacity: 0;
        transform: translateY(20px);
        animation: quantum-appear 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }}
    
    @keyframes quantum-appear {{
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .quantum-response::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        background: linear-gradient(45deg, 
            rgba(255,0,68,0.1) 0%,
            rgba(255,0,255,0.1) 50%,
            rgba(255,0,68,0.1) 100%);
        animation: hologram-pulse 8s infinite linear;
        z-index: -1;
    }}
    
    @keyframes hologram-pulse {{
        0% {{ opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
        100% {{ opacity: 0.3; }}
    }}
    
    /* Neural Links */
    .neural-link {{
        display: inline-block;
        padding: 0.5rem 1.5rem;
        margin: 0.5rem;
        background: rgba(255,0,68,0.1);
        border-radius: 30px;
        border: 1px solid rgba(255,0,68,0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }}
    
    .neural-link:hover {{
        background: rgba(255,0,255,0.2);
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(255,0,255,0.3);
    }}
    
    /* Quantum Typography */
    .quantum-text {{
        font-size: 1.1rem;
        line-height: 1.8;
        color: rgba(255,255,255,0.9);
        text-shadow: 0 0 10px rgba(255,0,68,0.3);
    }}
    
    /* Particle System Simulation */
    .particles {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }}
    
    .particle {{
        position: absolute;
        width: 2px;
        height: 2px;
        background: var(--neon-red);
        border-radius: 50%;
        opacity: 0.6;
        animation: float infinite linear;
    }}
    
    @keyframes float {{
        0% {{ transform: translateY(0) translateX(0); opacity: 0.6; }}
        50% {{ transform: translateY(-100vh) translateX(100vw); opacity: 0.2; }}
        100% {{ transform: translateY(0) translateX(0); opacity: 0.6; }}
    }}
    
    /* Glowing Cursor Effect */
    .glow-cursor {{
        position: fixed;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,0,68,0.8), transparent 70%);
        pointer-events: none;
        transform: translate(-50%, -50%);
        z-index: 9999;
        mix-blend-mode: screen;
    }}
    
    /* Holographic Title */
    .holographic-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        background: linear-gradient(45deg, #ff0044, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 50px rgba(255,0,68,0.5);
        margin: 0;
        animation: title-glow 3s infinite alternate;
    }}
    
    @keyframes title-glow {{
        0% {{ text-shadow: 0 0 50px rgba(255,0,68,0.5); }}
        100% {{ text-shadow: 0 0 100px rgba(255,0,255,0.8); }}
    }}
    
    </style>
""", unsafe_allow_html=True)

# Add Particle System
st.markdown("""
    <div class="particles">
        <div class="particle" style="top: 10%; left: 20%; animation-duration: 10s;"></div>
        <div class="particle" style="top: 30%; left: 50%; animation-duration: 8s;"></div>
        <div class="particle" style="top: 70%; left: 80%; animation-duration: 12s;"></div>
        <div class="particle" style="top: 50%; left: 10%; animation-duration: 9s;"></div>
        <div class="particle" style="top: 90%; left: 40%; animation-duration: 11s;"></div>
    </div>
    <div class="glow-cursor"></div>
""", unsafe_allow_html=True)

# --------------------------
# HOLOGRAM INIT
# --------------------------
@st.cache_resource
def load_cognitive_engine():
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"Quantum Core Initialization Failed: {str(e)}")
        return None

model = load_cognitive_engine()

# --------------------------
# QUANTUM FUNCTIONS
# --------------------------
async def hyper_search(query):
    try:
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            with DDGS() as ddgs:
                results = await loop.run_in_executor(
                    executor, 
                    lambda: list(ddgs.text(query, max_results=7))
                )
                return results
    except Exception as e:
        st.error(f"Quantum Search Interference: {str(e)}")
        return []

def generate_compiled_answer(query, results):
    if not results:
        return "Quantum interference patterns unstable. Reformulate query."
    
    try:
        documents = [result['body'] for result in results]
        query_embedding = model.encode(query)
        doc_embeddings = model.encode(documents)
        
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        top_indices = np.argsort(similarities)[-3:][::-1]  # Top 3 results
        compiled_answer = " ".join([documents[i] for i in top_indices])
        
        return compiled_answer[:1200] + "..." if len(compiled_answer) > 1200 else compiled_answer
    except Exception as e:
        return f"Quantum Compilation Error: {str(e)}"

# --------------------------
# INTERFACE RENDERING
# --------------------------
def main():
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 class="holographic-title">IRA AI</h1>
        </div>
    """, unsafe_allow_html=True)

    query = st.text_input(" ", placeholder="🌀 ENTER NEURAL QUERY PATTERN...", key="search", label_visibility="collapsed").strip()

    if query:
        results = asyncio.run(hyper_search(query))
        compiled_answer = generate_compiled_answer(query, results)
        
        st.markdown(f"""
            <div class="quantum-response">
                <div class="quantum-text">
                    {compiled_answer}
                </div>
                <div style="margin-top: 2rem;">
                    <h3 style="color: var(--hologram-pink); border-bottom: 1px solid rgba(255,0,68,0.3); padding-bottom: 0.5rem;">Quantum Sources</h3>
                    {"".join(f'<div class="neural-link">{result["title"]}</div>' for result in results[:3])}
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
