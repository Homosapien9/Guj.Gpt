import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import asyncio
from concurrent.futures import ThreadPoolExecutor

# --------------------------
# QUANTUM INTERFACE ENGINE
# --------------------------
st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'About': "⚡ HOLOGRAPHIC COGNITION INTERFACE v10.0 ⚡"}
)

# --------------------------
# CINEMATIC STYLING
# --------------------------
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Ubuntu+Mono&display=swap');
    
    :root {{
        --void-black: #0a0a12;
        --neon-purple: #8a2be2;
        --matrix-green: #00ff9d;
        --hologram-blue: #00f3ff;
        --cyber-pink: #ff00ff;
        --deep-space: linear-gradient(45deg, #12001f, #000000);
    }}
    
    body {{
        background: var(--deep-space);
        overflow-x: hidden;
        min-height: 100vh;
        font-family: 'Ubuntu Mono', monospace;
    }}
    
    /* Particle Horizon */
    .particle-layer {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background-image: 
            radial-gradient(circle at 50% 50%, 
                rgba(138,43,226,0.1) 0%, 
                transparent 60%),
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 3px,
                rgba(138,43,226,0.1) 3px,
                rgba(138,43,226,0.1) 6px
            );
        animation: space-drift 40s linear infinite;
    }}
    
    /* Cyber Input Matrix */
    .stTextInput>div>div>input {{
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid var(--neon-purple) !important;
        border-radius: 0 !important;
        padding: 1.5rem 0 !important;
        font-size: 2rem !important;
        color: var(--matrix-green) !important;
        box-shadow: 0 0 30px rgba(138,43,226,0.2) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-bottom: 2px solid var(--cyber-pink) !important;
        box-shadow: 0 0 50px rgba(255,0,255,0.3) !important;
        background: rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* Neural Pulse Animations */
    @keyframes neural-pulse {{
        0% {{ opacity: 0.2; transform: scale(1); }}
        50% {{ opacity: 1; transform: scale(1.05); }}
        100% {{ opacity: 0.2; transform: scale(1); }}
    }}
    
    @keyframes space-drift {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 1000px 1000px; }}
    }}
    
    /* Holographic Cards */
    .quantum-card {{
        background: linear-gradient(145deg, 
            rgba(18,0,31,0.9), 
            rgba(10,10,18,0.9)) !important;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        border: 1px solid transparent;
        border-image: linear-gradient(45deg, #8a2be2, #00f3ff) 1;
        animation: card-float 6s ease-in-out infinite;
        backdrop-filter: blur(10px);
    }}
    
    @keyframes card-float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .quantum-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(138,43,226,0.2),
            transparent
        );
        animation: matrix-scan 4s linear infinite;
    }}
    
    @keyframes matrix-scan {{
        0% {{ transform: translate(-50%, -50%) rotate(45deg) scale(2); }}
        100% {{ transform: translate(50%, 50%) rotate(45deg) scale(2); }}
    }}
    
    /* Cyber Suggestions */
    .neon-suggestion {{
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(90deg, 
            rgba(138,43,226,0.1), 
            rgba(0,243,255,0.05));
        position: relative;
        cursor: pointer;
        transition: all 0.3s ease;
        clip-path: polygon(0 0, 95% 0, 100% 50%, 95% 100%, 0 100%, 5% 50%);
    }}
    
    .neon-suggestion:hover {{
        background: linear-gradient(90deg, 
            rgba(138,43,226,0.3), 
            rgba(0,243,255,0.2));
        transform: translateX(20px);
    }}
    
    .neon-suggestion::after {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.1),
            transparent
        );
        animation: suggestion-glow 1.5s infinite;
    }}
    
    @keyframes suggestion-glow {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    /* Holographic Loader */
    .hologram-loader {{
        width: 80px;
        height: 80px;
        position: relative;
        margin: 2rem auto;
    }}
    
    .hologram-loader::before {{
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border: 3px solid var(--neon-purple);
        border-top-color: var(--cyber-pink);
        border-bottom-color: var(--hologram-blue);
        border-radius: 50%;
        animation: hologram-spin 1.5s linear infinite;
        filter: drop-shadow(0 0 10px var(--neon-purple));
    }}
    
    @keyframes hologram-spin {{
        0% {{ transform: rotate(0deg) scale(1); }}
        50% {{ transform: rotate(180deg) scale(1.2); }}
        100% {{ transform: rotate(360deg) scale(1); }}
    }}
    </style>
""", unsafe_allow_html=True)

# Add background layer
st.components.v1.html("""
    <div class="particle-layer"></div>
""")

# --------------------------
# AI CORE SYSTEM
# --------------------------
@st.cache_resource
def load_cognitive_engine():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    suggestion_base = [
        "Neural cryptography breakthroughs", 
        "Quantum teleportation protocols",
        "Dark matter harvesting", 
        "Neuro-synthetic interfaces",
        "Exoplanet terraforming", 
        "AI consciousness mapping"
    ]
    suggestion_embeddings = model.encode(suggestion_base)
    return model, suggestion_base, suggestion_embeddings

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
                return results[:9]
    except Exception as e:
        st.error(f"QUANTUM INTERFERENCE: {str(e)}")
        return []

@st.cache_data(ttl=300, show_spinner=False)
def neural_suggest(query):
    query_embed = model.encode([query])
    sim_scores = cosine_similarity(query_embed, suggestion_embeddings)[0]
    return [suggestions[i] for i in np.argsort(sim_scores)[-3:][::-1]]

# --------------------------
# INTERFACE RENDERING
# --------------------------
def main():
    st.markdown("""
        <div style="text-align: center; margin: 5rem 0;">
            <h1 style="
                font-family: 'Orbitron', sans-serif;
                font-size: 4rem;
                background: linear-gradient(45deg, #8a2be2, #00f3ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 50px rgba(138,43,226,0.5);
                animation: neural-pulse 2s infinite;
                margin-bottom: 2rem;
            ">
                NEXUS COGNITION ENGINE
            </h1>
            <div style="
                border-bottom: 2px solid #8a2be2;
                width: 50%;
                margin: 0 auto;
                box-shadow: 0 0 30px rgba(138,43,226,0.3);
            "></div>
        </div>
    """, unsafe_allow_html=True)

    query = st.text_input(" ", placeholder="ENTER QUANTUM QUERY VECTOR...", 
                         key="search", label_visibility="collapsed").strip()

    if query:
        with st.container():
            suggestions = neural_suggest(query)
            if suggestions:
                st.markdown("#### ACTIVE NEURAL PATTERNS")
                cols = st.columns(3)
                for i, sug in enumerate(suggestions):
                    with cols[i % 3]:
                        st.markdown(f"""
                            <div class="neon-suggestion" 
                                onclick="this.style.transform='scale(0.95)'; 
                                setTimeout(() => {{ document.querySelector('input').value = '{sug}'; }}, 200)">
                                <span style="color: var(--hologram-blue);">◈</span>
                                <span style="color: white; margin-left: 10px;">{sug}</span>
                            </div>
                        """, unsafe_allow_html=True)

        with st.spinner(""):
            st.markdown("""
                <div class="hologram-loader"></div>
                <div style="text-align: center; color: var(--neon-purple); 
                        margin: 1rem 0; font-size: 1.2em; animation: neural-pulse 2s infinite;">
                    DECRYPTING QUANTUM DATASTREAMS...
                </div>
            """, unsafe_allow_html=True)
            
            results = asyncio.run(hyper_search(query))
            
            if results:
                st.markdown("#### HOLOGRAPHIC RESULTS MATRIX")
                for result in results:
                    st.markdown(f"""
                        <div class="quantum-card">
                            <div style="border-left: 3px solid var(--cyber-pink); 
                                    padding-left: 1rem; margin-bottom: 1.5rem;">
                                <h3 style="color: var(--matrix-green); margin: 0;
                                        text-shadow: 0 0 15px rgba(0,255,157,0.3);">
                                    {result['title']}
                                </h3>
                            </div>
                            <p style="color: rgba(255,255,255,0.9); 
                                    line-height: 1.6; position: relative;">
                                <span style="color: var(--hologram-blue);">⫸⫸</span>
                                {result['body']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center; padding: 2rem; 
                            border: 2px solid var(--neon-purple);
                            color: var(--cyber-pink);
                            margin-top: 2rem;
                            animation: neural-pulse 1.5s infinite;">
                        ⚠️ QUANTUM FLUX DETECTED - NO STABLE RESULTS FOUND
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
