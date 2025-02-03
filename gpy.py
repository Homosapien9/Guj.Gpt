import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import asyncio
from concurrent.futures import ThreadPoolExecutor
from streamlit.components.v1 import html
import re

# --------------------------
# QUANTUM CORE INIT
# --------------------------
st.set_page_config(
    page_title="IRA AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'About': "⚛️ HOLOGRAPHIC COGNITION MATRIX v9.11"}
)

# --------------------------
# NEURAL INTERFACE STYLING
# --------------------------
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Syne+Mono&family=Major+Mono+Display&display=swap');
    
    :root {{
        --neon-red: #ff0044;
        --hologram-pink: #ff00ff;
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
    
    /* Quantum Entanglement Effect */
    @keyframes quantum-entanglement {{
        0% {{ transform: translate(0,0) scale(1); opacity: 1; }}
        50% {{ transform: translate(100px,50px) scale(1.5); opacity: 0.3; }}
        100% {{ transform: translate(0,0) scale(1); opacity: 1; }}
    }}
    
    /* Holographic Grid System */
    .holo-grid {{
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background-image: 
            linear-gradient(rgba(255,0,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,0,255,0.05) 1px, transparent 1px);
        background-size: 100px 100px;
        animation: grid-flow 40s linear infinite;
        z-index: -1;
    }}
    
    @keyframes grid-flow {{
        0% {{ transform: translate(0,0); }}
        100% {{ transform: translate(100px,100px); }}
    }}
    
    /* Particle Nebula */
    .quantum-nebula {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
    }}
    
    .nebula-particle {{
        position: absolute;
        width: 2px;
        height: 2px;
        background: var(--hologram-pink);
        border-radius: 50%;
        animation: particle-dance 15s infinite linear;
    }}
    
    @keyframes particle-dance {{
        0% {{ transform: translate(0,0) scale(1); opacity: 0.8; }}
        50% {{ transform: translate(100vw,50vh) scale(2); opacity: 0.2; }}
        100% {{ transform: translate(0,0) scale(1); opacity: 0.8; }}
    }}
    
    /* Enhanced Response Display */
    .quantum-response {{
        position: relative;
        padding: 2rem;
        margin: 2rem 0;
        background: linear-gradient(145deg, rgba(18,0,31,0.4), rgba(10,10,18,0.6));
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255,0,68,0.3);
        animation: quantum-appear 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .response-content {{
        font-size: 1.1rem;
        line-height: 1.8;
        text-shadow: 0 0 10px rgba(255,0,68,0.3);
    }}
    
    /* Clickable Neural Links */
    .neural-link {{
        display: block;
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(255,0,68,0.1);
        border-radius: 15px;
        border: 1px solid rgba(255,0,68,0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        animation: link-glow 3s infinite alternate;
    }}
    
    .neural-link:hover {{
        background: rgba(255,0,255,0.2);
        transform: translateX(10px);
    }}
    
    @keyframes link-glow {{
        0% {{ box-shadow: 0 0 10px rgba(255,0,68,0.1); }}
        100% {{ box-shadow: 0 0 30px rgba(255,0,255,0.2); }}
    }}
    
    /* Quantum Input Field */
    .stTextInput>div>div>input {{
        background: rgba(0,0,0,0.3) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1.5rem 2rem !important;
        font-size: 1.2rem !important;
        color: var(--neon-red) !important;
        box-shadow: 0 0 50px rgba(255,0,68,0.3) !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    /* Floating Code Matrix */
    .code-matrix {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
        opacity: 0.1;
    }}
    
    .matrix-line {{
        position: absolute;
        color: var(--hologram-pink);
        font-family: 'Major Mono Display', monospace;
        animation: matrix-fall 20s linear infinite;
    }}
    
    @keyframes matrix-fall {{
        0% {{ transform: translateY(-100vh); opacity: 0; }}
        2% {{ opacity: 1; }}
        100% {{ transform: translateY(100vh); opacity: 0; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HOLOGRAPHIC BACKGROUND
# --------------------------
st.markdown("""
    <div class="holo-grid"></div>
    <div class="quantum-nebula" id="quantumNebula"></div>
    <div class="code-matrix" id="codeMatrix"></div>
""", unsafe_allow_html=True)

# --------------------------
# QUANTUM MODULES
# --------------------------
@st.cache_resource
def load_cognitive_engine():
    return SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

class QuantumCore:
    def __init__(self):
        self.model = load_cognitive_engine()
        self.history = []
        
    async def hyper_search(self, query):
        try:
            with DDGS() as ddgs:
                return await asyncio.get_event_loop().run_in_executor(
                    ThreadPoolExecutor(), 
                    lambda: list(ddgs.text(query, max_results=7))
                )
        except Exception as e:
            st.error(f"Quantum flux detected: {str(e)}")
            return []
    
    def generate_response(self, query, results):
        documents = [result['body'] for result in results]
        query_embedding = self.model.encode(query)
        doc_embeddings = self.model.encode(documents)
        
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        top_indices = np.argsort(similarities)[-3:][::-1]
        compiled = self._format_response(" ".join([documents[i] for i in top_indices]))
        
        return {
            'content': compiled,
            'sources': [results[i] for i in top_indices],
            'confidence': np.mean(similarities[top_indices])
        }
    
    def _format_response(self, text):
        # Improve text formatting
        text = re.sub(r'(?<=[a-z])\.(?=\s[A-Z])', '.\n\n', text)  # Paragraph breaks
        text = re.sub(r'(\d+)\.\s', r'\1. ', text)  # Fix numbered lists
        return text

# --------------------------
# MAIN INTERFACE
# --------------------------
def main():
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 style="font-family: 'Orbitron', sans-serif; font-size: 4rem;
                    background: linear-gradient(45deg, #ff0044, #ff00ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    animation: quantum-entanglement 5s infinite;">
                IRA AI
            </h1>
        </div>
    """, unsafe_allow_html=True)

    if 'core' not in st.session_state:
        st.session_state.core = QuantumCore()
    
    query = st.text_input(" ", placeholder="🌠 ENTER QUANTUM QUERY PATTERN...", 
                        key="search", label_visibility="collapsed").strip()
    
    if query:
        with st.spinner('🌀 Entangling quantum states...'):
            results = asyncio.run(st.session_state.core.hyper_search(query))
            response = st.session_state.core.generate_response(query, results)
            
            # Response Display
            response_html = f"""
            <div class="quantum-response">
                <div class="response-content">
                    {response['content']}
                </div>
                <div style="margin-top: 2rem;">
                    <h3 style="color: var(--hologram-pink); border-bottom: 1px solid rgba(255,0,68,0.3);">
                        Quantum Sources (Click to Warp)
                    </h3>
                    {"".join(
                        f'<a href="{result["href"]}" target="_blank" class="neural-link">'
                        f'<span style="color: var(--neon-red);">⇲</span> {result["title"]}</a>'
                        for result in response['sources']
                    )}
                </div>
            </div>
            """
            st.markdown(response_html, unsafe_allow_html=True)
            
            # Quantum Effects
            html(f"""
            <script>
            // Create new particles
            for(let i=0; i<20; i++) {{
                const particle = document.createElement('div');
                particle.className = 'nebula-particle';
                particle.style.left = Math.random()*100 + 'vw';
                particle.style.top = Math.random()*100 + 'vh';
                particle.style.animationDuration = Math.random()*10 + 5 + 's';
                document.getElementById('quantumNebula').appendChild(particle);
            }}
            
            // Add matrix code effect
            const codeMatrix = document.getElementById('codeMatrix');
            const characters = '01';
            for(let i=0; i<50; i++) {{
                const line = document.createElement('div');
                line.className = 'matrix-line';
                line.style.left = Math.random()*100 + 'vw';
                line.style.animationDelay = Math.random()*5 + 's';
                line.textContent = Array(30).fill().map(() => 
                    characters[Math.floor(Math.random()*characters.length)]
                ).join(' ');
                codeMatrix.appendChild(line);
            }}
            </script>
            """)

if __name__ == "__main__":
    main()
