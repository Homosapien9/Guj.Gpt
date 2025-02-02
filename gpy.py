import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import aiohttp
import asyncio
import torch
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
# NEURAL INTERFACE STYLING
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
        --particle-glow: radial-gradient(circle at center, 
            rgba(0,243,255,0.15) 0%, 
            transparent 70%);
    }}
    
    body {{
        background: var(--depth-space);
        overflow-x: hidden;
        perspective: 1000px;
    }}
    
    .cyber-input {{
        background: rgba(0,0,0,0.3) !important;
        border: none !important;
        padding: 2rem 3rem !important;
        font-size: 2.2rem !important;
        color: var(--cyber-green) !important;
        border-radius: 15px !important;
        transform-style: preserve-3d;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 0 50px rgba(0,243,255,0.1);
        position: relative;
        backdrop-filter: blur(10px);
    }}
    
    .cyber-input:focus {{
        transform: translateZ(50px) scale(1.05);
        box-shadow: 0 0 100px rgba(0,243,255,0.3),
                    0 0 50px rgba(138,43,226,0.3);
    }}
    
    .quantum-card {{
        background: linear-gradient(145deg, 
            rgba(16,16,26,0.95), 
            rgba(32,32,48,0.95)) !important;
        border: 1px solid rgba(138,43,226,0.5);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        transform: rotateX(15deg) translateZ(0);
        transition: all 0.6s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .quantum-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: var(--particle-glow);
        animation: plasma-drift 15s linear infinite;
    }}
    
    .quantum-card:hover {{
        transform: rotateX(0deg) translateZ(50px) scale(1.05);
        box-shadow: 0 30px 50px rgba(0,0,0,0.5);
    }}
    
    .neon-suggestion {{
        padding: 1.5rem;
        margin: 1rem 0;
        background: rgba(138,43,226,0.1);
        border-radius: 12px;
        cursor: pointer;
        transform: skewX(-5deg);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
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
            rgba(0,243,255,0.2),
            transparent
        );
        transition: left 0.6s ease;
    }}
    
    .neon-suggestion:hover {{
        transform: skewX(0deg) translateX(30px);
        background: rgba(138,43,226,0.3);
    }}
    
    .neon-suggestion:hover::after {{
        left: 100%;
    }}
    
    @keyframes plasma-drift {{
        0% {{ transform: rotate(0deg) translate(0,0); }}
        100% {{ transform: rotate(360deg) translate(100px,50px); }}
    }}
    
    .hologram-loader {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        position: relative;
        animation: hologram-spin 2s linear infinite;
        margin: 2rem auto;
    }}
    
    .hologram-loader::before {{
        content: '';
        position: absolute;
        inset: -10px;
        border-radius: 50%;
        border: 5px solid var(--hologram-blue);
        border-top-color: transparent;
        filter: drop-shadow(0 0 20px var(--hologram-blue));
    }}
    
    @keyframes hologram-spin {{
        0% {{ transform: rotate(0deg) scale(1); }}
        50% {{ transform: rotate(180deg) scale(1.2); }}
        100% {{ transform: rotate(360deg) scale(1); }}
    }}
    
    .cyber-header {{
        font-family: 'Orbitron', sans-serif !important;
        text-align: center;
        font-size: 5rem !important;
        background: linear-gradient(
            45deg,
            var(--hologram-blue),
            var(--plasma-purple),
            var(--cyber-green)
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 3rem 0;
        text-shadow: 0 0 50px rgba(0,243,255,0.3);
        position: relative;
    }}
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HOLOGRAPHIC BACKGROUND
# --------------------------
st.components.v1.html("""
<script>
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    document.body.appendChild(canvas);
    
    let particles = [];
    const particleCount = 300;
    
    class Particle {
        constructor() {
            this.reset();
        }
        
        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.radius = Math.random() * 2;
            this.color = `hsl(${Math.random() * 360}, 100%, 50%)`;
            this.alpha = Math.random() * 0.5;
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            
            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
            
            this.alpha = 0.3 + Math.sin(Date.now() * 0.001 + this.x) * 0.2;
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.alpha;
            ctx.fill();
        }
    }
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        particles = Array.from({length: particleCount}, () => new Particle());
    }
    
    function animate() {
        ctx.fillStyle = 'rgba(0,1,25,0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(p => {
            p.update();
            p.draw();
            
            particles.forEach(p2 => {
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    ctx.beginPath();
                    ctx.strokeStyle = p.color;
                    ctx.globalAlpha = 0.3 - (distance / 150);
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(animate);
    }
    
    window.addEventListener('resize', resize);
    resize();
    animate();
});
</script>
""")

# --------------------------
# AI CORE SYSTEM
# --------------------------
@st.cache_resource
def load_cognitive_engine():
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

model, suggestions, suggestion_embeddings = load_cognitive_engine()

# --------------------------
# QUANTUM FUNCTIONS
# --------------------------
async def hyper_search(query):
    try:
        with DDGS() as ddgs:
            return [r for r in ddgs.text(query, max_results=7)]
    except Exception as e:
        st.error(f"QUANTUM DISRUPTION: {str(e)}")
        return []

@st.cache_data(ttl=300)
def neural_suggest(query):
    query_embed = model.encode([query])
    sim_scores = cosine_similarity(query_embed, suggestion_embeddings)[0]
    return [suggestions[i] for i in np.argsort(sim_scores)[-4:][::-1]]

# --------------------------
# INTERFACE RENDERING
# --------------------------
def main():
    st.markdown("""
        <h1 class="cyber-header">
            <span style="display: block; transform: skewX(-10deg);">
                HYPERION SEARCH
            </span>
        </h1>
    """, unsafe_allow_html=True)
    
    # Quantum Input Field
    query = st.text_input(" ", placeholder="▣ ENTER NEURAL QUERY VECTOR...", 
                         key="search", label_visibility="collapsed",
                         help="Initiate quantum pattern recognition sequence").strip()
    
    # Neural Suggestions
    if query:
        with st.container():
            suggestions = neural_suggest(query)
            if suggestions:
                st.markdown("""
                    <div style="margin: 2rem 0; border-left: 4px solid var(--cyber-green);
                                padding-left: 2rem; transform: skewX(10deg);">
                        <h3 style="color: var(--neon-pink); margin-bottom: 1rem;
                                text-shadow: 0 0 20px rgba(255,0,255,0.3);">
                            COGNITIVE PATTERN MATCHES
                        </h3>
                """, unsafe_allow_html=True)
                
                for sug in suggestions:
                    st.markdown(f"""
                        <div class="neon-suggestion" onclick="this.style.transform='scale(0.9)'; 
                            setTimeout(() => {{ document.getElementById('search').value = '{sug}'; }}, 300)">
                            <span style="color: var(--hologram-blue); font-size: 1.2em;">◈</span>
                            <span style="color: white; margin-left: 1rem; font-size: 1.1em;">{sug}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    # Quantum Results
    if query:
        with st.spinner("""
            <div class="hologram-loader"></div>
            <div style="text-align: center; color: var(--cyber-green); 
                     margin-top: 1rem; font-size: 1.2em;">
                SCANNING COSMIC DATABANKS...
            </div>
        """):
            results = asyncio.run(hyper_search(query))
            
            if results:
                query_embed = model.encode([query])
                result_texts = [f"{r['title']} {r['body']}" for r in results]
                result_embeddings = model.encode(result_texts)
                similarities = cosine_similarity(query_embed, result_embeddings)[0]
                
                st.markdown("""
                    <div style="margin: 4rem 0 2rem 0;">
                        <h2 style="color: var(--plasma-purple); 
                                border-bottom: 3px solid var(--hologram-blue);
                                padding-bottom: 1rem; display: inline-block;
                                transform: skewX(-10deg);">
                            QUANTUM ENTANGLEMENT RESULTS
                        </h2>
                    </div>
                """, unsafe_allow_html=True)
                
                for i, result in enumerate(results):
                    st.markdown(f"""
                        <div class="quantum-card">
                            <div style="display: flex; justify-content: space-between; 
                                     align-items: center; margin-bottom: 1.5rem;">
                                <h3 style="color: var(--hologram-blue); margin: 0;
                                        text-shadow: 0 0 15px rgba(0,243,255,0.3);">
                                    {result['title']}
                                </h3>
                                <div style="background: rgba(0,255,136,0.1); 
                                         padding: 0.5rem 1rem; border-radius: 8px;
                                         border: 1px solid var(--cyber-green);">
                                    <span style="color: var(--cyber-green); 
                                              font-family: 'Orbitron', sans-serif;">
                                        COHERENCE: {similarities[i]*100:.1f}%
                                    </span>
                                </div>
                            </div>
                            <p style="color: rgba(255,255,255,0.9); line-height: 1.6;
                                    font-size: 1.1em;">
                                {result['body']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("ZERO MATCH FOUND IN QUANTUM FOAM")

if __name__ == "__main__":
    main()
