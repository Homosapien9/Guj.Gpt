import streamlit as st
from duckduckgo_search import DDGS
import time
from textblob import TextBlob

# Configuration
SAFE_SEARCH_FILTERS = {"safesearch": "strict", "max_results": 12}

# Streamlit Cloud Optimized Page Config
st.set_page_config(
    page_title="Nexus Quantum",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Premium CSS Design (Cloud-Optimized)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    :root {{
        --primary: #00f7ff;
        --secondary: #7a00ff;
        --background: #0a0a1a;
    }}

    * {{
        font-family: 'Inter', sans-serif;
        transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .main {{
        background: var(--background);
        color: #ffffff;
    }}

    .stTextInput>div>div>input {{
        color: var(--primary) !important;
        background: rgba(0, 247, 255, 0.05) !important;
        border: 2px solid rgba(0, 247, 255, 0.3) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        font-size: 1.1rem !important;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 30px rgba(0, 247, 255, 0.1);
    }}

    .stTextInput>div>div>input:focus {{
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 247, 255, 0.2) !important;
    }}

    .quantum-card {{
        background: linear-gradient(145deg, rgba(10, 10, 30, 0.9), rgba(20, 20, 50, 0.7));
        border: 1px solid rgba(0, 247, 255, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(6px);
    }}

    .quantum-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 40px rgba(0, 247, 255, 0.15);
    }}

    .ai-badge {{
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        color: #000 !important;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
    }}

    .pro-glow {{
        position: relative;
        overflow: hidden;
    }}

    .pro-glow::after {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            transparent 25%,
            var(--primary),
            transparent 75%
        );
        animation: rotate 4s linear infinite;
        z-index: -1;
    }}

    @keyframes rotate {{
        100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=3600, show_spinner=False)
def enhanced_search(query):
    """Cloud-optimized search with caching"""
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, **SAFE_SEARCH_FILTERS))
    except Exception as e:
        st.error(f"Quantum flux detected: {str(e)}")
        return []

def analyze_context(query):
    """AI-powered context analysis"""
    analysis = TextBlob(query)
    return {
        "sentiment": analysis.sentiment.polarity,
        "subjectivity": analysis.sentiment.subjectivity,
        "tags": analysis.noun_phrases
    }

# Main Interface
st.markdown("<h1 style='text-align:center; margin-bottom:2rem;'>🌐 NEXUS QUANTUM</h1>", unsafe_allow_html=True)

# Search Core
query = st.text_input("", placeholder="Enter quantum query...", key="main_search", label_visibility="collapsed")

if query:
    start_time = time.time()
    
    with st.spinner('Analyzing quantum patterns...'):
        results = enhanced_search(query)
        context = analyze_context(query)

        # AI Insights Panel
        with st.expander("🔍 Quantum Insights", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sentiment Score", f"{context['sentiment']:.2f}")
                st.metric("Subjectivity", f"{context['subjectivity']:.2f}")
            with col2:
                st.write("**Key Concepts:**")
                for tag in context['tags'][:3]:
                    st.markdown(f"- `{tag}`")

        # Search Results
        if results:
            for result in results:
                with st.container():
                    st.markdown(f"""
                        <div class='quantum-card pro-glow'>
                            <div class='ai-badge'>AI Verified</div>
                            <h3>{result['title']}</h3>
                            <a href="{result['href']}" target="_blank" style='color: var(--primary);'>{result['href']}</a>
                            <p style='color: #ccf; margin-top:0.75rem;'>{result['body']}</p>
                        </div>
                    """, unsafe_allow_html=True)

            # Performance Footer
            end_time = time.time()
            st.markdown(f"""
                <div style='text-align:center; color: var(--primary); margin:2rem 0;'>
                    ⚡ Quantum resolution achieved in {end_time - start_time:.2f}s
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center; color: var(--primary);'>No temporal matches found</p>", unsafe_allow_html=True)

# Authored Footer
st.markdown("""
    <div style='text-align:center; padding:2rem; color: rgba(0, 247, 255, 0.5);'>
        NEXUS QUANTUM v2.3 • Secure AI-Powered Search
    </div>
""", unsafe_allow_html=True)
