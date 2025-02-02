import streamlit as st
import asyncio
import aiohttp
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from duckduckgo_search import DDGS  # Updated DuckDuckGo Search

# Configuration moved to top for better visibility
STREAMLIT_CONFIG = {
    "page_title": "◈ IRA AI",
    "page_icon": "🌑",
    "layout": "centered",
    "initial_sidebar_state": "collapsed",
    "menu_items": {'About': "### ◈ INFINITE RECURSIVE ARCHITECT v9.6.2 ◈"}
}

MODEL_CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "cache_expiry": 3600  # 1 hour cache
}

API_CONFIG = {
    "coingecko_url": "https://api.coingecko.com/api/v3/simple/price",
    "crypto_ids": "bitcoin,ethereum",
    "timeout": aiohttp.ClientTimeout(total=10)
}

# Initialize Streamlit configuration
st.set_page_config(**STREAMLIT_CONFIG)

# Simplified CSS for better compatibility
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@900&display=swap');
    
    .neural-input {{
        font-size: 2.5rem !important;
        padding: 2rem !important;
        text-align: center;
        color: #00FFEA !important;
        background: transparent !important;
        border: none !important;
        margin: 2rem 0;
    }}
    
    .result-card {{
        background: rgba(0,0,0,0.7) !important;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #2A00FF;
    }}
    
    .matrix-fall {{
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
    }}
    
    @keyframes matrix-fall {{
        0% {{ transform: translateY(-100%); }}
        100% {{ transform: translateY(0%); }}
    }}
    </style>
""", unsafe_allow_html=True)

# Cache resources and data properly
@st.cache_resource(ttl=MODEL_CONFIG["cache_expiry"])
def load_model():
    return SentenceTransformer(MODEL_CONFIG["model_name"])

@st.cache_data(ttl=300)  # Cache crypto prices for 5 minutes
async def fetch_live_data():
    try:
        async with aiohttp.ClientSession(timeout=API_CONFIG["timeout"]) as session:
            params = {"ids": API_CONFIG["crypto_ids"], "vs_currencies": "usd"}
            async with session.get(API_CONFIG["coingecko_url"], params=params) as response:
                return await response.json()
    except Exception as e:
        st.error(f"Error fetching live data: {str(e)}")
        return None

async def search_web(query):
    try:
        with DDGS() as ddgs:
            return [r for r in ddgs.text(query, max_results=5)]
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

# Main application logic
def main():
    model = load_model()
    
    with st.container():
        st.markdown("""
            <h1 style="
                font-family: 'Exo 2', sans-serif;
                text-align: center;
                font-size: 4rem;
                margin: 2rem 0;
                color: #00FFEA;
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

    if query:
        with st.spinner("SYNCHRONIZING NEURAL MATRICES..."):
            search_results = await search_web(query)
            
            if search_results:
                query_embedding = model.encode([query])
                result_texts = [f"{r['title']} {r['body']}" for r in search_results]
                result_embeddings = model.encode(result_texts)
                similarities = cosine_similarity(query_embedding, result_embeddings)[0]

                st.markdown("### QUANTUM SEARCH RESULTS")
                for i, result in enumerate(search_results):
                    st.markdown(f"""
                        <div class="result-card">
                            <h3 style="color: #00FFEA;">{result['title']}</h3>
                            <p style="color: #FF00AA;">{result['body']}</p>
                            <p style="color: #2A00FF;">Similarity: {similarities[i]:.2f}</p>
                        </div>
                    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("### REAL-TIME DATA STREAM")
        live_data = await fetch_live_data()
        if live_data:
            st.write(live_data)

# Run the async application
if __name__ == "__main__":
    asyncio.run(main())
