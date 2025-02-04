import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
import random

# --------------------------
# QUANTUMQUEST CORE INIT
# --------------------------
st.set_page_config(
    page_title="QuantumQuest",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={'About': "⚛️ QUANTUMQUEST COGNITION MATRIX v10.0"}
)

# --------------------------
# NEURAL INTERFACE STYLING
# --------------------------
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Syne+Mono&family=Major+Mono+Display&display=swap');
    
    :root {{
        --neon-purple: #8A2BE2;
        --matrix-green: #00ff00;
        --quantum-gradient: linear-gradient(135deg, #0a0a1a 0%, #1a0033 100%);
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
    
    /* Welcome Panel */
    .welcome-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0,0,0,0.95);
        z-index: 9999;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(10px);
        animation: slideIn 1s cubic-bezier(0.4, 0, 0.2, 1), 
                   slideOut 1s cubic-bezier(0.4, 0, 0.2, 1) 3s forwards;
        transform-origin: top center;
    }}
    
    @keyframes slideIn {{
        0% {{ transform: translateY(-100vh) scaleY(0); opacity: 0; }}
        100% {{ transform: translateY(0) scaleY(1); opacity: 1; }}
    }}
    
    @keyframes slideOut {{
        0% {{ transform: translateY(0) scaleY(1); opacity: 1; }}
        100% {{ transform: translateY(100vh) scaleY(0); opacity: 0; }}
    }}
    
    .welcome-content {{
        position: relative;
        padding: 4rem;
        border-radius: 20px;
        text-align: center;
        overflow: hidden;
        perspective: 1000px;
    }}
    
    .holographic-border {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, 
            rgba(138,43,226,0.2),
            rgba(75,0,130,0.4),
            rgba(138,43,226,0.2));
        animation: hologram 4s linear infinite;
        z-index: -1;
    }}
    
    @keyframes hologram {{
        0% {{ opacity: 0.8; transform: rotate(0deg); }}
        100% {{ opacity: 0.8; transform: rotate(360deg); }}
    }}
    
    .quantum-particles span {{
        position: absolute;
        background: var(--neon-purple);
        border-radius: 50%;
        pointer-events: none;
        animation: particle-float 3s infinite;
    }}
    
    @keyframes particle-float {{
        0%, 100% {{ transform: translateY(0) translateX(0); opacity: 0; }}
        50% {{ transform: translateY(-100px) translateX(50px); opacity: 1; }}
    }}
    
    /* Enhanced Title Animation */
    .welcome-title {{
        animation: title-glow 2s ease-in-out infinite alternate,
                   title-float 3s ease-in-out infinite;
    }}
    
    @keyframes title-glow {{
        0% {{ text-shadow: 0 0 10px var(--neon-purple); }}
        100% {{ text-shadow: 0 0 30px var(--neon-purple); }}
    }}
    
    @keyframes title-float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    /* Enhanced Enter Button */
    .enter-button {{
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        transform-style: preserve-3d;
    }}
    
    .enter-button:hover {{
        transform: scale(1.1) rotateX(15deg) rotateY(15deg);
        box-shadow: 0 0 40px rgba(138,43,226,0.5);
    }}
    
    .enter-button::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 25%,
            rgba(138,43,226,0.2) 50%,
            transparent 75%);
        animation: button-scan 3s linear infinite;
    }}
    
    @keyframes button-scan {{
        0% {{ transform: translateX(-100%) rotate(45deg); }}
        100% {{ transform: translateX(100%) rotate(45deg); }}
    }}
    
    /* Matrix Rain Effect */
    .matrix-rain {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
        opacity: 0.5;
    }}
    
    .matrix-line {{
        position: absolute;
        color: var(--neon-purple);
        font-family: 'Major Mono Display', monospace;
        font-size: 1.2rem;
        animation: matrix-fall 10s linear infinite;
        text-shadow: 0 0 10px rgba(138,43,226,0.5);
    }}
    
    @keyframes matrix-fall {{
        0% {{ transform: translateY(-100vh); opacity: 0; }}
        2% {{ opacity: 1; }}
        100% {{ transform: translateY(100vh); opacity: 0; }}
    }}
    
    /* Quantum Response */
    .quantum-response {{
        border: 1px solid rgba(138,43,226,0.3);
        background: linear-gradient(145deg, rgba(26,0,51,0.4), rgba(10,10,26,0.6));
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 20px;
        backdrop-filter: blur(10px);
        animation: fadeIn 1s ease;
    }}
    
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .neural-link {{
        display: block;
        padding: 1rem;
        margin: 1rem 0;
        background: rgba(138,43,226,0.1);
        border-radius: 15px;
        border: 1px solid rgba(138,43,226,0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        animation: link-glow 3s infinite alternate;
    }}
    
    .neural-link:hover {{
        background: rgba(138,43,226,0.2);
        transform: translateX(10px);
    }}
    
    @keyframes link-glow {{
        0% {{ box-shadow: 0 0 5px rgba(138,43,226,0.3); }}
        100% {{ box-shadow: 0 0 20px rgba(138,43,226,0.5); }}
    }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# WELCOME PANEL
# --------------------------
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

if st.session_state.first_visit:
    particles = "".join(
        f'<span style="width: {random.randint(2,6)}px; height: {random.randint(2,6)}px; '
        f'top: {random.randint(10,90)}%; left: {random.randint(10,90)}%; '
        f'animation-delay: {random.random()*2}s;"></span>'
        for _ in range(30)
    )
    
    st.markdown(f"""
    <div class="welcome-overlay">
        <div class="welcome-content">
            <div class="holographic-border"></div>
            <div class="quantum-particles">{particles}</div>
            <h1 class="welcome-title" style="font-family: 'Orbitron'; font-size: 4rem; color: var(--neon-purple); margin: 2rem;">
                QUANTUMQUEST INITIALIZED
            </h1>
            <p style="font-family: 'Syne Mono'; color: var(--neon-purple); margin: 1.5rem;">
                █▓▒░ HYPERSPACE MATRIX ONLINE ░▒▓█
            </p>
            <button class="enter-button" onclick="window.parent.document.querySelector('.stApp').dispatchEvent(new CustomEvent('CLOSE_WELCOME'))"
                style="background: transparent; border: 2px solid var(--neon-purple); padding: 1rem 3rem; border-radius: 8px;
                font-family: 'Syne Mono'; color: white; font-size: 1.2rem; position: relative;">
                ENTER QUANTUM FIELD
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle the close event
    st.components.v1.html("""
    <script>
    document.querySelector('.stApp').addEventListener('CLOSE_WELCOME', function() {
        window.parent.document.querySelector('[class^="welcome-overlay"]').style.display = 'none';
    });
    </script>
    """)
    st.session_state.first_visit = False

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
                    lambda: list(ddgs.text(query, max_results=15))
                )
        except Exception as e:
            st.error(f"Quantum flux detected: {str(e)}")
            return []
    
    def generate_response(self, query, results):
        random.shuffle(results)
        documents = [result['body'] for result in results]
        query_embedding = self.model.encode(query)
        doc_embeddings = self.model.encode(documents)
        
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        top_indices = np.argsort(similarities)[-10:][::-1]  
        compiled = self._format_response(" ".join([documents[i] for i in top_indices]))
        
        return {
            'content': compiled,
            'sources': [results[i] for i in top_indices],
            'confidence': np.mean(similarities[top_indices])
        }
    
    def _format_response(self, text):
        # Improve text formatting
        text = re.sub(r'(?<=[a-z])\.(?=\s[A-Z])', '.\n\n', text) 
        text = re.sub(r'(\d+)\.\s', r'\1. ', text) 
        text = re.sub(r'\s+', ' ', text)  
        return text

# --------------------------
# MAIN INTERFACE
# --------------------------
def main():
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 class="main-title">QuantumQuest</h1>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="matrix-rain" id="codeMatrix"></div>
    <script>
    function createMatrix() {
        const container = document.getElementById('codeMatrix');
        const characters = '01';
        
        for(let i = 0; i < 150; i++) {  // Increased matrix rain density
            const line = document.createElement('div');
            line.className = 'matrix-line';
            line.style.left = Math.random() * 100 + 'vw';
            line.style.animationDuration = Math.random() * 5 + 5 + 's';
            line.textContent = Array(100).fill().map(() => 
                characters[Math.floor(Math.random() * characters.length)]
            ).join(' ');
            container.appendChild(line);
        }
    }
    createMatrix();
    </script>
    """, unsafe_allow_html=True)

    if 'core' not in st.session_state:
        st.session_state.core = QuantumCore()
    
    query = st.text_input(" ", placeholder="🌠 ENTER QUANTUM QUERY ...", 
                        key="search", label_visibility="collapsed").strip()
    
    if query:
        with st.spinner('🌀 Entangling quantum states...'):
            results = asyncio.run(st.session_state.core.hyper_search(query))
            response = st.session_state.core.generate_response(query, results)

            response_html = f"""
            <div class="quantum-response">
                <div class="response-content">
                    {response['content']}
                </div>
                <div style="margin-top: 2rem;">
                    <h3 style="color: var(--neon-purple); border-bottom: 1px solid rgba(138,43,226,0.3);">
                        Quantum Sources (Click to Warp)
                    </h3>
                    {"".join(
                        f'<a href="{result["href"]}" target="_blank" class="neural-link">'
                        f'<span style="color: var(--neon-purple);">⇲</span> {result["title"]}</a>'
                        for result in response['sources']
                    )}
                </div>
            </div>
            """
            st.markdown(response_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
