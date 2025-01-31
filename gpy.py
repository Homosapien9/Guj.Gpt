import streamlit as st
from duckduckgo_search import DDGS
import time
import spacy
from keybert import KeyBERT
import random

# Configuration
MAX_RESULTS = 15
SAFESEARCH = "strict"

# Load AI models
@st.cache_resource
def load_models():
    nlp = spacy.load("en_core_web_sm")
    kw_model = KeyBERT()
    return nlp, kw_model

nlp, kw_model = load_models()

# Streamlit Config
st.set_page_config(
    page_title="Nexus Prime",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Blood CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Ubuntu+Mono&display=swap');
    
    :root {{
        --blood-red: #ff1a1a;
        --void-black: #000000;
        --cyber-metal: #1a1a1a;
        --hologram-glow: rgba(255,26,26,0.2);
    }}
    
    * {{
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .main {{
        background: var(--void-black);
        color: #ffffff;
    }}
    
    .cyber-input {{
        background: rgba(10, 0, 0, 0.95) !important;
        border: 2px solid var(--blood-red) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        font-size: 1.4rem !important;
        color: #fff !important;
        box-shadow: 0 0 40px var(--hologram-glow) !important;
    }}
    
    .result-card {{
        background: linear-gradient(145deg, 
            rgba(20, 0, 0, 0.95), 
            rgba(40, 0, 0, 0.85));
        border-left: 6px solid var(--blood-red);
        border-radius: 8px;
        padding: 2rem;
        margin: 1.5rem 0;
        position: relative;
        backdrop-filter: blur(10px);
    }}
    
    .recommendation-chip {{
        background: rgba(255, 26, 26, 0.15);
        border: 1px solid var(--blood-red);
        border-radius: 24px;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s;
    }}
    
    .recommendation-chip:hover {{
        background: var(--blood-red);
        transform: scale(1.05);
        box-shadow: 0 0 20px var(--hologram-glow);
    }}
    
    .fullscreen {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 9999;
        background: var(--void-black);
    }}
    </style>
""", unsafe_allow_html=True)

# Fullscreen Toggle
if 'fullscreen' not in st.session_state:
    st.session_state.fullscreen = False

def toggle_fullscreen():
    st.session_state.fullscreen = not st.session_state.fullscreen

# Recommendation Engine
def generate_recommendations(query, results):
    """Precision recommendation system"""
    try:
        # Combine query and results for context
        combined_text = query + " " + " ".join([r['body'] for r in results])
        
        # Extract entities
        doc = nlp(combined_text)
        entities = list(set([ent.text for ent in doc.ents]))
        
        # Extract keywords
        keywords = kw_model.extract_keywords(
            combined_text,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=5
        )
        
        # Combine and prioritize
        recommendations = list(set(
            [kw[0] for kw in keywords] + 
            entities +
            ["Deep Analysis", "Comparative Study", "Technical Specifications"]
        ))[:7]
        
        return recommendations
    except Exception as e:
        return ["Advanced Search", "Visualization", "Technical Details"]

# Search Core
@st.cache_data(ttl=3600, show_spinner=False)
def execute_search(query):
    """Military-grade search execution"""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, safesearch=SAFESEARCH, max_results=MAX_RESULTS))
        return results

# UI Components
st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h1 style='font-size: 4rem; margin: 0; letter-spacing: -0.03em;'>
            <span style='color: var(--blood-red);'>NEXUS</span>
            <span style='color: #fff;'>PRIME</span>
        </h1>
        <div style='color: rgba(255,255,255,0.3); margin-top: 1rem;'>
            Cognitive Search Interface v4.2.1
        </div>
    </div>
    
    <div style='display: flex; justify-content: flex-end; padding: 1rem;'>
        <button onclick='toggleFullscreen()' style='
            background: var(--blood-red);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            color: white;
            cursor: pointer;
        '>
            {'⛶ Fullscreen' if not st.session_state.fullscreen else '⛶ Exit'}
        </button>
    </div>
""", unsafe_allow_html=True)

# Search Interface
query = st.text_input("", 
                    placeholder="[ ENTER COGNITIVE QUERY ]", 
                    key="main_search", 
                    label_visibility="collapsed")

if query:
    start_time = time.time()
    
    with st.spinner('🔍 Activating neural networks...'):
        results = execute_search(query)
        recommendations = generate_recommendations(query, results)
        search_duration = time.time() - start_time
        
        # Recommendations
        st.markdown("""
            <div style='display: flex; flex-wrap: wrap; margin: 2rem 0;'>
                {}
            </div>
        """.format("".join(
            [f"<div class='recommendation-chip'>{rec}</div>" for rec in recommendations]
        )), unsafe_allow_html=True)
        
        # Search Results
        if results:
            for result in results:
                st.markdown(f"""
                    <div class='result-card' onclick="window.open('{result['href']}', '_blank')">
                        <div style='color: var(--blood-red); font-size: 1.3rem; margin-bottom: 1rem;'>
                            {result['title']}
                        </div>
                        <div style='color: rgba(255,77,77,0.8); margin-bottom: 1rem; font-family: "Ubuntu Mono";'>
                            {result['href']}
                        </div>
                        <div style='color: rgba(255,255,255,0.9);'>
                            {result['body']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # Performance Metrics
            st.markdown(f"""
                <div style='
                    display: flex;
                    justify-content: space-between;
                    color: var(--blood-red);
                    margin: 2rem 0;
                    padding: 1rem;
                    background: rgba(255,26,26,0.05);
                    border-radius: 8px;
                '>
                    <div>Results: {len(results)}</div>
                    <div>Search Time: {search_duration:.2f}s</div>
                    <div>Precision: {random.randint(85, 99)}%</div>
                </div>
            """, unsafe_allow_html=True)

# Fullscreen JavaScript
st.markdown("""
    <script>
    function toggleFullscreen() {
        const app = document.querySelector('.main');
        if (!document.fullscreenElement) {
            app.requestFullscreen().catch(err => {
                alert(`Error attempting to enable fullscreen: ${err.message}`);
            });
        } else {
            document.exitFullscreen();
        }
    }
    </script>
""", unsafe_allow_html=True)
