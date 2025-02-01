import streamlit as st
import time
import random
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import ddg  # Updated import
from streamlit.components.v1 import html
import aiohttp
import asyncio
from pyinstrument import Profiler

# Singularity Configuration
st.set_page_config(
    page_title="◈ IRA AI",
    page_icon="🌑",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "### ◈ INFINITE RECURSIVE ARCHITECT v9.6.2 ◈"
    }
)

# Event Horizon Styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@1200&family=Cyborg&family=Exo+2:wght@900&display=swap');
    
    :root {{
        --void-core: #000000;
        --neon-abyss: linear-gradient(135deg, 
            #2A00FF 0%, 
            #FF00AA 30%, 
            #00FFEA 70%);
        --quantum-plasma: #2A00FF;
        --tachyon-speed: 0.2s;
    }}
    
    body {{
        background: var(--void-core);
        overflow: hidden;
        perspective: 1000px;
    }}
    
    .quantum-void {{
        position: fixed;
        width: 300vw;
        height: 300vh;
        background: 
            radial-gradient(circle at 50% 50%, 
                rgba(42,0,255,0.05) 0%, 
                transparent 70%),
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 2px,
                rgba(255,0,170,0.02) 3px,
                rgba(255,0,170,0.02) 4px
            );
        animation: singularity-drift 60s linear infinite;
        z-index: -9999;
    }}
    
    @keyframes singularity-drift {{
        0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
        100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
    }}
    
    .hologram-interface {{
        position: relative;
        padding: 5rem;
        margin: 5rem auto;
        background: transparent;
        transform-style: preserve-3d;
    }}
    
    .neural-input {{
        background: transparent !important;
        border: none !important;
        padding: 4rem !important;
        font-size: 3.5rem !important;
        color: #00FFEA !important;
        text-align: center;
        text-shadow: 0 0 80px #2A00FF;
        position: relative;
        width: 100%;
        transition: all var(--tachyon-speed);
    }}
    
    .neural-input::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0%;
        height: 5px;
        background: var(--neon-abyss);
        transition: all var(--tachyon-speed);
    }}
    
    .neural-input:focus::after {{
        width: 100%;
        left: 0;
        box-shadow: 0 0 100px #FF00AA;
    }}
    
    .quantum-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
        gap: 4rem;
        padding: 2rem;
        transform: translateZ(50px);
    }}
    
    .data-stream {{
        height: 600px;
        background: linear-gradient(135deg, 
            rgba(0,0,0,0.98) 0%, 
            rgba(0,255,234,0.05) 100%);
        position: relative;
        overflow: hidden;
    }}
    
    </style>
""", unsafe_allow_html=True)

# Quantum Void Background
html("""
<div class="quantum-void"></div>
<canvas id="neuralNetwork" style="
    position: fixed;
    top: 0;
    left: 0;
    z-index: -9998;
    pointer-events: none;
"></canvas>

<script>
const canvas = document.getElementById('neuralNetwork');
const ctx = canvas.getContext('2d');
let nodes = [];

class Node {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.2;
        this.vy = (Math.random() - 0.5) * 0.2;
        this.radius = Math.random() * 2;
        this.color = `hsl(${Math.random() * 360}, 100%, 50%)`;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
}

function init() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    nodes = Array.from({ length: 500 }, () => new Node());
}

function animate() {
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    nodes.forEach(node => {
        node.update();
        
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.fill();
        
        nodes.forEach(other => {
            const dx = node.x - other.x;
            const dy = node.y - other.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 150) {
                ctx.beginPath();
                ctx.strokeStyle = `rgba(42,0,255,${1 - distance/150})`;
                ctx.lineWidth = 0.3;
                ctx.moveTo(node.x, node.y);
                ctx.lineTo(other.x, other.y);
                ctx.stroke();
            }
        });
    });
    
    requestAnimationFrame(animate);
}

init();
window.addEventListener('resize', init);
animate();

// Neural Interaction
document.addEventListener('mousemove', (e) => {
    nodes.forEach(node => {
        const dx = e.clientX - node.x;
        const dy = e.clientY - node.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 200) {
            node.vx += dx * 0.00005;
            node.vy += dy * 0.00005;
        }
    });
});
</script>
""")

# Load Sentence Transformer Model
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# Async DuckDuckGo Search
async def search_web(query):
    results = ddg(query, max_results=5)  # Updated usage
    return results

# Real-Time Data Fetching (Example: Cryptocurrency Prices)
async def fetch_live_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# IRA AI Interface Core
with st.container():
    st.markdown("""
        <div class="hologram-interface">
            <h1 style="
                font-family: 'Exo 2', sans-serif;
                text-align: center;
                font-size: 6rem;
                margin: 2rem 0;
                background: var(--neon-abyss);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 100px #2A00FF;
                letter-spacing: 0.8rem;
                position: relative;
                z-index: 999;
            ">
                IRA AI
            </h1>
    """, unsafe_allow_html=True)

    query = st.text_input(
        " ",
        placeholder="◈ ENTER NEURAL QUERY ◈",
        key="neural_search",
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Quantum Response Sequence
if query:
    with st.spinner("SYNCHRONIZING NEURAL MATRICES..."):
        # Profile the search and processing
        profiler = Profiler()
        profiler.start()

        # Perform DuckDuckGo search
        search_results = asyncio.run(search_web(query))
        
        # Encode query and results
        query_embedding = model.encode([query])
        result_embeddings = model.encode([result['title'] + " " + result['body'] for result in search_results])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, result_embeddings)[0]
        
        profiler.stop()
        
        # Display results
        st.markdown("### QUANTUM SEARCH RESULTS")
        for i, result in enumerate(search_results):
            st.markdown(f"""
                <div style="
                    background: rgba(0,0,0,0.5);
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 1rem 0;
                ">
                    <h3 style="color: #00FFEA;">{result['title']}</h3>
                    <p style="color: #FF00AA;">{result['body']}</p>
                    <p style="color: #2A00FF;">Similarity: {similarities[i]:.2f}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Display profiling results
        st.markdown("### PERFORMANCE ANALYSIS")
        st.text(profiler.output_text(unicode=True, color=True))

# Real-Time Data Stream
with st.container():
    st.markdown("### REAL-TIME DATA STREAM")
    live_data = asyncio.run(fetch_live_data())
    st.write(live_data)

# Quantum Grid Visualization
with st.container():
    st.markdown("""
        <div class="quantum-grid">
            <div class="data-stream">
                <div style="
                    position: absolute;
                    width: 100%;
                    height: 200%;
                    background: repeating-linear-gradient(
                        90deg,
                        transparent,
                        transparent 20px,
                        rgba(0,255,234,0.1) 21px,
                        rgba(0,255,234,0.1) 40px
                    );
                    animation: matrix-fall 15s linear infinite;
                "></div>
            </div>
        </div>
        
        <style>
        @keyframes matrix-fall {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(0%); }
        }
        </style>
    """, unsafe_allow_html=True)
