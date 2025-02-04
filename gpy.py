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
        animation: fade-out 1s ease 3s forwards;
    }}
    
    .welcome-content {{
        background: linear-gradient(145deg, #1a0033, #0a0a1a);
        padding: 3rem;
        border-radius: 20px;
        border: 2px solid var(--neon-purple);
        text-align: center;
        box-shadow: 0 0 50px rgba(138,43,226,0.5);
    }}
    
    /* Matrix Rain */
    .code-matrix {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: -1;
        opacity: 0.3;
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
    
    /* Enter Button */
    .enter-button {{
        background: var(--neon-purple);
        border: none;
        padding: 1rem 2rem;
        border-radius: 50px;
        cursor: pointer;
        font-family: 'Syne Mono';
        color: white;
        animation: neon-pulse 2s infinite;
    }}
    
    @keyframes neon-pulse {{
        0% {{ box-shadow: 0 0 5px var(--neon-purple); }}
        50% {{ box-shadow: 0 0 20px var(--neon-purple); }}
        100% {{ box-shadow: 0 0 5px var(--neon-purple); }}
    }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# WELCOME PANEL
# --------------------------
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True

if st.session_state.first_visit:
    st.markdown("""
    <div class="welcome-overlay">
        <div class="welcome-content">
            <h1 class="welcome-title" style="font-family: 'Orbitron'; font-size: 4rem; color: var(--neon-purple);">
                WELCOME TO QUANTUMQUEST
            </h1>
            <p style="font-family: 'Syne Mono'; color: var(--neon-purple);">
                Initializing quantum cognition matrix...
            </p>
            <button class="enter-button" onclick="window.parent.document.querySelector('.stApp').dispatchEvent(new CustomEvent('CLOSE_WELCOME'))">
                ENTER THE QUANTUM REALM
            </button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle the close event
    html("""
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
    <div class="code-matrix" id="codeMatrix"></div>
    <script>
    function createMatrix() {
        const container = document.getElementById('codeMatrix');
        const characters = '01';
        
        for(let i = 0; i < 150; i++) {  // Increased matrix rain density
            const line = document.createElement('div');
            line.className = 'matrix-line';
            line.style.left = math.random() * 100 + 'vw';
            line.style.animationDuration = math.random() * 5 + 5 + 's';
            line.textContent = Array(100).fill().map(() => 
                characters[math.floor(math.random() * characters.length)]
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
if __name__ == "__main__":
    main()
