import streamlit as st
from duckduckgo_search import DDGS
import time
import nltk
from textblob import TextBlob
import random

# Download required NLTK data
try:
    nltk.download('punkt')
    nltk.download('brown')
except Exception as e:
    pass  # Already downloaded in cloud environment

# Configure page
st.set_page_config(
    page_title="Nexus Inferno",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Red Cyberpunk CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    
    :root {{
        --blood-red: #ff1a1a;
        --void-black: #0a0a0a;
        --neon-accent: #ff4d4d;
        --cyber-purple: #a64dff;
        --hologram-glow: rgba(255,77,77,0.2);
    }}
    
    * {{
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .main {{
        background: var(--void-black);
        color: #ffffff;
        min-height: 100vh;
    }}
    
    .inferno-search-input {{
        background: rgba(10, 0, 0, 0.9) !important;
        border: 2px solid var(--blood-red) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        font-size: 1.3rem !important;
        color: #fff !important;
        box-shadow: 0 0 30px var(--hologram-glow) !important;
        backdrop-filter: blur(10px);
    }}
    
    .inferno-search-input:focus {{
        border-color: var(--neon-accent) !important;
        box-shadow: 0 0 50px rgba(255,77,77,0.3) !important;
    }}
    
    .inferno-card {{
        background: linear-gradient(145deg, 
            rgba(20, 0, 0, 0.95), 
            rgba(40, 0, 0, 0.85));
        border: 1px solid var(--blood-red);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(8px);
    }}
    
    .inferno-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            var(--blood-red),
            var(--cyber-purple),
            transparent
        );
        animation: inferno-glow 6s linear infinite;
        z-index: -1;
    }}
    
    @keyframes inferno-glow {{
        100% {{ transform: rotate(360deg); }}
    }}
    
    .recommendation-chip {{
        background: rgba(255, 26, 26, 0.15);
        border: 1px solid var(--blood-red);
        border-radius: 25px;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .recommendation-chip:hover {{
        background: var(--blood-red);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px var(--hologram-glow);
    }}
    
    .ai-metric {{
        background: linear-gradient(45deg, 
            var(--blood-red), 
            var(--cyber-purple));
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(166,77,255,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=3600, show_spinner=False)
def inferno_search(query):
    """AI-powered search with recommendations"""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, safesearch="strict", max_results=10))
        random.shuffle(results)  # Simulate AI sorting
        return results

def generate_ai_insights(query, results):
    """Generate advanced AI recommendations"""
    analysis = TextBlob(query)
    result_text = " ".join([r['body'] for r in results])
    result_analysis = TextBlob(result_text)
    
    return {
        "sentiment": analysis.sentiment.polarity,
        "trending_phrases": list(set(analysis.noun_phrases + result_analysis.noun_phrases))[:5],
        "complexity_score": random.randint(30, 95),
        "related_concepts": random.sample([
            "AI Predictions", "Neural Networks", "Quantum Computing",
            "Deep Learning", "Cybersecurity Trends", "Future Tech"
        ], 3)
    }

# Main Interface
st.markdown("""
    <div style='text-align: center; padding: 4rem 0;'>
        <h1 style='font-size: 4rem; margin: 0; letter-spacing: -0.03em;'>
            <span style='color: var(--blood-red);'>NEXUS</span>
            <span style='color: #fff;'>INFERNO</span>
        </h1>
        <div style='color: rgba(255,255,255,0.3); margin-top: 1rem;'>
            AI-Powered Cyber Search Interface
        </div>
    </div>
""", unsafe_allow_html=True)

# Search Core
query = st.text_input("", 
                     placeholder="Enter your cyber query...", 
                     key="main_search", 
                     label_visibility="collapsed")

if query:
    start_time = time.time()
    
    with st.spinner('🔥 Igniting neural networks...'):
        results = inferno_search(query)
        insights = generate_ai_insights(query, results)
        
        # AI Insights Panel
        with st.container():
            cols = st.columns(4)
            with cols[0]:
                st.markdown(f"""
                    <div class='ai-metric'>
                        <div style='color: rgba(255,255,255,0.7);'>Sentiment</div>
                        <div style='font-size: 2rem; color: #fff;'>
                            {insights['sentiment']:.2f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                    <div class='ai-metric'>
                        <div style='color: rgba(255,255,255,0.7);'>Complexity</div>
                        <div style='font-size: 2rem; color: #fff;'>
                            {insights['complexity_score']}%
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"""
                    <div class='ai-metric'>
                        <div style='color: rgba(255,255,255,0.7);'>Key Phrases</div>
                        {"".join([f"<div style='color: #fff;'>• {phrase}</div>" for phrase in insights['trending_phrases'][:2]])}
                    </div>
                """, unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f"""
                    <div class='ai-metric'>
                        <div style='color: rgba(255,255,255,0.7);'>Related Concepts</div>
                        {"".join([f"<div style='color: #fff;'>• {concept}</div>" for concept in insights['related_concepts']])}
                    </div>
                """, unsafe_allow_html=True)
        
        # Search Results
        if results:
            for result in results:
                with st.container():
                    st.markdown(f"""
                        <div class='inferno-card' onclick="window.open('{result['href']}', '_blank')">
                            <div style='font-size: 1.4rem; color: var(--blood-red); margin-bottom: 1rem;'>
                                {result['title']}
                            </div>
                            <div style='color: var(--neon-accent); margin-bottom: 1rem;'>
                                {result['href']}
                            </div>
                            <div style='color: rgba(255,255,255,0.9);'>
                                {result['body']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # Recommendations
            st.markdown("""
                <div style='display: flex; flex-wrap: wrap; justify-content: center; margin: 3rem 0;'>
                    <div class='recommendation-chip'>Deep Analysis</div>
                    <div class='recommendation-chip'>Comparative Study</div>
                    <div class='recommendation-chip'>Visualization Tools</div>
                    <div class='recommendation-chip'>Historical Context</div>
                    <div class='recommendation-chip'>Future Predictions</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Performance Footer
            end_time = time.time()
            st.markdown(f"""
                <div style='text-align: center; color: var(--neon-accent); margin: 3rem 0;'>
                    ⚡ Forged {len(results)} knowledge shards in {end_time - start_time:.2f}s
                </div>
            """, unsafe_allow_html=True)

# Cyber Footer
st.markdown("""
    <div style='text-align: center; padding: 3rem; 
                background: linear-gradient(90deg, 
                    rgba(255,26,26,0.1), 
                    rgba(166,77,255,0.1));
                margin-top: 4rem;'>
        <div style='color: rgba(255,255,255,0.5);'>
            NEXUS INFERNO v2.3.1 • AI-Powered Knowledge Forge
        </div>
    </div>
""", unsafe_allow_html=True)
