import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS
import asyncio
from concurrent.futures import ThreadPoolExecutor
import math
# --------------------------
# PAGE CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="IRA AI",
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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Russo+One&family=Zen+Dots&display=swap');
    
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
        font-family: 'Russo One', sans-serif;
        color: white;
    }}
    
    /* Interactive Particle Background */
    .particle-layer {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: radial-gradient(circle at 50% 50%, rgba(138,43,226,0.05), transparent 60%);
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
    
    /* Holographic Cards */
    .quantum-card {{
        background: linear-gradient(145deg, rgba(18,0,31,0.9), rgba(10,10,18,0.9)) !important;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
        overflow: hidden;
        border: 1px solid transparent;
        border-image: linear-gradient(45deg, #8a2be2, #00f3ff) 1;
        animation: card-float 6s ease-in-out infinite;
        backdrop-filter: blur(10px);
        transform-style: preserve-3d;
    }}
    
    .quantum-card:hover {{
        transform: rotateX(10deg) rotateY(10deg) scale(1.05);
        box-shadow: 0 0 50px rgba(138,43,226,0.5);
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
        background: linear-gradient(45deg, transparent, rgba(138,43,226,0.2), transparent);
        animation: matrix-scan 4s linear infinite;
    }}
    
    @keyframes matrix-scan {{
        0% {{ transform: translate(-50%, -50%) rotate(45deg) scale(2); }}
        100% {{ transform: translate(50%, 50%) rotate(45deg) scale(2); }}
    }}
    
    /* Hologram Loader */
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
    
    /* Text Effects */
    .neon-text {{
        font-family: 'Orbitron', sans-serif;
        font-size: 4rem;
        background: linear-gradient(45deg, #8a2be2, #00f3ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 50px rgba(138,43,226,0.5);
        animation: neural-pulse 2s infinite;
    }}
    
    @keyframes neural-pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    </style>
""", unsafe_allow_html=True)

# Add interactive particle background
st.components.v1.html("""
    <div class="particle-layer"></div>
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
        const particleCount = 200;
        
        class Particle {
            constructor() {
                this.reset();
            }
            
            reset() {
                this.x = math.random() * canvas.width;
                this.y = math.random() * canvas.height;
                this.vx = (math.random() - 0.5) * 0.5;
                this.vy = (math.random() - 0.5) * 0.5;
                this.radius = math.random() * 2;
                this.color = `hsl(${math.random() * 360}, 100%, 50%)`;
                this.alpha = math.random() * 0.5;
            }
            
            update() {
                this.x += this.vx;
                this.y += this.vy;
                
                if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
                
                this.alpha = 0.3 + math.sin(Date.now() * 0.001 + this.x) * 0.2;
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
    return model

model = load_cognitive_engine()

# --------------------------
# QUANTUM FUNCTIONS
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
                return results[:20]
    except Exception as e:
        st.error(f"QUANTUM INTERFERENCE: {str(e)}")
        return []

# --------------------------
# INTERFACE RENDERING
# --------------------------
def main():
    st.markdown("""
        <div style="text-align: center; margin: 5rem 0;">
            <h1 class="neon-text">
                IRA AI
            </h1>
            <div style="border-bottom: 2px solid #8a2be2; width: 50%; margin: 0 auto;"></div>
        </div>
    """, unsafe_allow_html=True)

    query = st.text_input(" ", placeholder="ENTER QUANTUM QUERY VECTOR...", key="search", label_visibility="collapsed").strip()

    if query:
        with st.spinner("Decrypting Quantum Datastructures..."):
            st.markdown("""<div class="hologram-loader"></div>""", unsafe_allow_html=True)
            
            results = asyncio.run(hyper_search(query))
            
            if results:
                st.markdown("#### HOLOGRAPHIC RESULTS MATRIX")
                for result in results:
                    st.markdown(f"""
                        <div class="quantum-card">
                            <div style="border-left: 3px solid var(--cyber-pink); padding-left: 1rem;">
                                <h3 style="color: var(--matrix-green);">{result['title']}</h3>
                            </div>
                            <p style="color: rgba(255,255,255,0.9);">{result['body']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center; padding: 2rem; color: var(--cyber-pink); border: 2px solid var(--neon-purple); margin-top: 2rem;">
                        ⚠️ QUANTUM FLUX DETECTED - NO STABLE RESULTS FOUND
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
