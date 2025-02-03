import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import asyncio
from concurrent.futures import ThreadPoolExecutor
from streamlit.components.v1 import html
import time
from textblob import TextBlob
import matplotlib.pyplot as plt
from scipy import stats
import speech_recognition as sr

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
        --void-black: #0a0a12;
        --neon-red: #ff0044;
        --hologram-pink: #ff00ff;
        --quantum-gradient: radial-gradient(circle at 50% 50%, #180028, #000000);
        --glow-intensity: 1;
        --primary-hue: 240;
        --secondary-hue: 300;
    }}
    
    body {{
        background: var(--quantum-gradient);
        font-family: 'Syne Mono', monospace;
        color: #fff;
        overflow-x: hidden;
        margin: 0;
        padding: 0;
        animation: reality-shift 60s infinite alternate;
    }}
    
    /* Animations */
    @keyframes quantum-entrance {{
        0% {{ opacity: 0; transform: scale(0.5) rotate(360deg); filter: blur(20px); }}
        100% {{ opacity: 1; transform: scale(1) rotate(0deg); filter: blur(0px); }}
    }}
    
    @keyframes hologram-pulse {{
        0% {{ opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
        100% {{ opacity: 0.3; }}
    }}
    
    @keyframes neural-pulse {{
        0% {{ transform: scale(1); opacity: 0.8; }}
        50% {{ transform: scale(1.05); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.8; }}
    }}
    
    /* Interface Elements */
    .holographic-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        background: linear-gradient(45deg, #ff0044, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 50px rgba(255,0,68,0.5);
        margin: 0;
        animation: neural-pulse 3s infinite;
    }}
    
    .quantum-input {{
        background: rgba(0,0,0,0.2) !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 1.5rem 2rem !important;
        font-size: 1.5rem !important;
        color: var(--neon-red) !important;
        box-shadow: 0 0 50px rgba(255,0,68,0.3) !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    .quantum-response {{
        position: relative;
        padding: 2rem;
        margin: 2rem 0;
        background: linear-gradient(145deg, rgba(18,0,31,0.4), rgba(10,10,18,0.4));
        backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255,0,68,0.3);
        animation: quantum-entrance 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .neural-link {{
        display: inline-block;
        padding: 0.5rem 1.5rem;
        margin: 0.5rem;
        background: rgba(255,0,68,0.1);
        border-radius: 30px;
        border: 1px solid rgba(255,0,68,0.3);
        transition: all 0.3s ease;
        cursor: pointer;
        animation: neural-pulse 3s infinite;
    }}
    
    /* Advanced Features */
    .temporal-graph {{
        height: 300px;
        background: rgba(255,0,68,0.1);
        border-radius: 20px;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
    }}
    
    .sentiment-indicator {{
        width: 100%;
        height: 5px;
        background: rgba(255,255,255,0.1);
        border-radius: 3px;
        margin: 1rem 0;
    }}
    
    .quantum-console {{
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 300px;
        background: rgba(0,0,0,0.3);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(255,0,68,0.3);
    }}
    
    /* Background Elements */
    .entangled-particle {{
        position: fixed;
        width: 2px;
        height: 2px;
        background: #ff00ff;
        border-radius: 50%;
        pointer-events: none;
        animation: quantum-entanglement 2s infinite;
    }}
    
    @keyframes quantum-entanglement {{
        0% {{ transform: translate(0,0); opacity: 1; }}
        50% {{ transform: translate(100px,50px); opacity: 0.3; }}
        100% {{ transform: translate(0,0); opacity: 1; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HOLOGRAPHIC BACKGROUND
# --------------------------
st.markdown("""
    <div class="entangled-particle" style="top:20%;left:30%"></div>
    <div class="entangled-particle" style="top:70%;left:80%"></div>
    <div class="entangled-particle" style="top:40%;left:65%"></div>
    <div class="quantum-console" id="quantumConsole">
        <div class="console-line">⚛️ System Operational</div>
        <div class="console-line">🌌 Quantum Link Stable</div>
        <div class="console-line">🌀 Neural Net Ready</div>
    </div>
""", unsafe_allow_html=True)

# --------------------------
# QUANTUM MODULES
# --------------------------
@st.cache_resource
def load_cognitive_engine():
    try:
        return SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        st.error(f"Quantum Core Failure: {str(e)}")
        return None

class NexusCore:
    def __init__(self):
        self.model = load_cognitive_engine()
        self.recognizer = sr.Recognizer()
        self.history = []
        
    async def hyper_search(self, query):
        try:
            with DDGS() as ddgs:
                return await asyncio.get_event_loop().run_in_executor(
                    ThreadPoolExecutor(), 
                    lambda: list(ddgs.text(query, max_results=7))
                )
        except Exception as e:
            st.error(f"Search Collapse: {str(e)}")
            return []
    
    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
    def generate_response(self, query, results):
        documents = [result['body'] for result in results]
        query_embedding = self.model.encode(query)
        doc_embeddings = self.model.encode(documents)
        
        similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
        top_indices = np.argsort(similarities)[-3:][::-1]
        compiled = " ".join([documents[i] for i in top_indices])
        
        return {
            'content': compiled[:1200] + "..." if len(compiled) > 1200 else compiled,
            'sentiment': self.analyze_sentiment(compiled),
            'confidence': np.mean(similarities[top_indices])
        }

# --------------------------
# INTERFACE COMPONENTS
# --------------------------
def render_voice_input():
    with st.expander("🎙️ Voice Interface"):
        with sr.Microphone() as source:
            audio = st.session_state.core.recognizer.listen(source)
            try:
                return st.session_state.core.recognizer.recognize_google(audio)
            except:
                return ""

def render_temporal_graph():
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.random.normal(1, 0.1, 100)
    ax.plot(x, y, color='#ff0044')
    ax.set_facecolor('black')
    plt.axis('off')
    st.pyplot(fig)

# --------------------------
# MAIN INTERFACE
# --------------------------
def main():
    st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <h1 class="holographic-title">NEXUS MATRIX</h1>
        </div>
    """, unsafe_allow_html=True)

    if 'core' not in st.session_state:
        st.session_state.core = NexusCore()
    
    # Input System
    col1, col2 = st.columns([3,1])
    with col1:
        query = st.text_input(" ", placeholder="🌌 ENTER HOLOGRAPHIC QUERY...", 
                            key="search", label_visibility="collapsed").strip()
    with col2:
        voice_query = render_voice_input()
    
    query = query or voice_query
    
    if query:
        with st.spinner('🌀 Entangling quantum states...'):
            results = asyncio.run(st.session_state.core.hyper_search(query))
            response = st.session_state.core.generate_response(query, results)
            
            # Response Display
            response_html = f"""
            <div class="quantum-response">
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <div class="confidence">🔼 Confidence: {response['confidence']:.2%}</div>
                    <div class="sentiment">🧠 Sentiment: {response['sentiment']:.2f}</div>
                </div>
                <div class="response-content">{response['content']}</div>
                <div style="margin-top: 2rem;">
                    <h3 style="color: var(--hologram-pink); border-bottom: 1px solid rgba(255,0,68,0.3);">
                        Quantum Sources
                    </h3>
                    {"".join(f'<div class="neural-link" onclick="window.open(\'{result["href"]}\')">{result["title"]}</div>' for result in results[:3])}
                </div>
            </div>
            """
            st.markdown(response_html, unsafe_allow_html=True)
            
            # Visualization
            render_temporal_graph()
            
            # System Console Update
            html(f"""
            <script>
            const consoleDiv = document.getElementById('quantumConsole');
            const newEntry = document.createElement('div');
            newEntry.className = 'console-line';
            newEntry.textContent = '🌀 Processed: {query.substring(0,15)}...';
            consoleDiv.appendChild(newEntry);
            </script>
            """)
            
        # Quantum Noise Effect
        html("""
        <script>
        function quantumEffect() {
            const particles = [];
            for(let i=0; i<50; i++) {
                const p = document.createElement('div');
                p.className = 'entangled-particle';
                p.style.left = math.random()*100 + 'vw';
                p.style.top = math.random()*100 + 'vh';
                document.body.appendChild(p);
                particles.push(p);
                setTimeout(() => p.remove(), 1000);
            }
        }
        quantumEffect();
        </script>
        """)

if __name__ == "__main__":
    main()
