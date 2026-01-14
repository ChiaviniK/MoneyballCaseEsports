import streamlit as st
import pandas as pd
import json
import time
import joblib

# --- Configuração da Página ---
st.set_page_config(
    page_title="NEXUS ANALYTICS",
    page_icon="👾",
    layout="wide"
)

# --- CSS CUSTOMIZADO: PIXEL ART + CYBERPUNK MINIMALISTA ---
st.markdown("""
<style>
    /* Importando Fontes: Pixelada para Títulos, Mono para Dados */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Roboto+Mono:wght@300;400;700&display=swap');

    /* --- Fundo e Cores Globais --- */
    .stApp {
        background-color: #0f0518; /* Roxo Quase Preto */
        color: #e0e0e0;
        font-family: 'Roboto Mono', monospace; /* Fonte estilo Terminal */
    }

    /* --- Tipografia Pixelada (Títulos) --- */
    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        text-transform: uppercase;
        line-height: 1.5;
    }
    
    /* Gradiente no Título Principal */
    h1 {
        background: -webkit-linear-gradient(45deg, #ff0055, #9900ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 0px rgba(255, 255, 255, 0.1);
    }

    /* --- Cards e Containers Minimalistas --- */
    div[data-testid="stMetric"], .stCode {
        background-color: #190b2f; /* Roxo Escuro */
        border: 1px solid #3d1e6d;
        border-radius: 4px; /* Cantos levemente arredondados, mas firmes */
        padding: 15px;
        box-shadow: 0 4px 0px #240e45; /* Sombra Sólida estilo Pixel */
    }

    /* --- Botões Arcade --- */
    .stButton>button {
        background-color: #ff0055; /* Vermelho Neon */
        color: white;
        font-family: 'Press Start 2P', cursive;
        font-size: 10px;
        border: none;
        border-radius: 0px;
        padding: 15px 30px;
        box-shadow: 4px 4px 0px #990044;
        transition: all 0.1s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #ff3377;
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #990044;
    }

    /* --- Inputs Estilo Console --- */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #0f0518;
        color: #00ffcc; /* Cyan para texto digitado */
        border: 1px solid #5a2d91;
        font-family: 'Roboto Mono', monospace;
    }

    /* --- Banner Header Customizado --- */
    .header-banner {
        width: 100%;
        height: 150px;
        background-image: url('https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
        border-bottom: 4px solid #ff0055;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.8;
    }
    .header-overlay {
        background: rgba(15, 5, 24, 0.7);
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* --- Ajuste de Métricas --- */
    div[data-testid="stMetricLabel"] { color: #bca0dc; font-size: 0.8rem; }
    div[data-testid="stMetricValue"] { color: #fff; font-family: 'Press Start 2P'; font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

# --- BANNER TOPO (HTML Puro) ---
st.markdown("""
<div class="header-banner">
    <div class="header-overlay">
        <h2 style="color: white; text-align: center; font-size: 25px;">INSERT COIN TO START</h2>
    </div>
</div>
""", unsafe_allow_html=True)

# --- HEADER E SIDEBAR ---
col_logo, col_title = st.columns([1, 5])
with col_title:
    st.title("NEXUS ANALYTICS")
    st.caption("AI-POWERED ESPORTS SCOUTING PLATFORM // VER. 3.0")

with st.sidebar:
    st.markdown("### SYSTEM STATUS")
    st.info("🟢 API GATEWAY: ONLINE")
    st.info("🟢 ML ENGINE: READY")
    st.markdown("---")
    st.write("**PRO MODE**")
    st.caption("Use este painel para monitorar partidas em tempo real e executar predições de vitória.")

st.markdown("---")

# --- SEÇÃO 1: API INGESTION ---
st.markdown("### 1. LIVE DATA INGESTION")
with st.container():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        api_key = st.text_input("RIOT API KEY", type="password", placeholder="RGAPI-XXXXXXXX")
    with c2:
        server = st.selectbox("REGION", ["BR1", "NA1", "KR", "EUW"])
    with c3:
        st.write("") # Espaço
        st.write("")
        btn_search = st.button("SEARCH MATCH")

    if btn_search:
        with st.spinner("ACCESSING RIOT SERVERS..."):
            time.sleep(1.5) # Simulação
            st.success("MATCH DATA RETRIEVED")
            
            # Layout de Métricas "Arcade"
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("GAME MODE", "RANKED")
            m2.metric("ELAPSED TIME", "18:42")
            m3.metric("GOLD DIFF", "+2.4k")
            m4.metric("DRAGONS", "2 / 0")
            
            # JSON visual
            st.markdown("**> RAW PAYLOAD**")
            st.code("""
{
  "gameId": 482910,
  "platformId": "BR1",
  "status": "IN_PROGRESS",
  "teams": [
    {"teamId": 100, "bans": ["Zed", "Lee Sin"], "gold": 24500},
    {"teamId": 200, "bans": ["Yasuo", "Yone"], "gold": 22100}
  ]
}
            """, language="json")

st.markdown("---")

# --- SEÇÃO 2: ML PREDICTION ---
st.markdown("### 2. WIN PROBABILITY (AI)")
st.caption("Carregue o JSON da partida para processar no modelo 'LogReg_v1'.")

col_upl, col_res = st.columns(2)

with col_upl:
    uploaded_file = st.file_uploader("UPLOAD MATCH JSON", type=["json"])
    
    if st.button("LOAD DEMO DATA (SIMULATION)"):
        st.session_state['match_data'] = {
            "gold_diff_15min": 3500,
            "blue_dragons": 3,
            "red_dragons": 0,
            "vision_score_diff": 25
        }
        st.info("DEMO DATA LOADED INTO MEMORY")

with col_res:
    # Tenta carregar o modelo
    try:
        model = joblib.load('lol_win_predictor.pkl')
        model_status = "ONLINE"
    except:
        model_status = "OFFLINE (MODEL NOT FOUND)"
        model = None

    # Visual do Status do Modelo
    st.markdown(f"""
    <div style="border: 1px solid #5a2d91; padding: 10px; background: #0f0518;">
        <span style="color: #bca0dc; font-size: 0.8rem;">MODEL ENGINE STATUS:</span><br>
        <span style="color: {'#00ffcc' if model else '#ff0055'}; font-family: 'Press Start 2P'; font-size: 0.9rem;">{model_status}</span>
    </div>
    """, unsafe_allow_html=True)

    # Executa a Predição
    if 'match_data' in st.session_state and model:
        st.markdown("<br>", unsafe_allow_html=True)
        data = st.session_state['match_data']
        
        # Previsão
        df_input = pd.DataFrame([data])
        proba = model.predict_proba(df_input)[0][1] # Probabilidade Blue Win
        
        # Visualização do Resultado
        st.markdown("#### > PREDICTION RESULT")
        if proba > 0.5:
            st.success(f"BLUE TEAM VICTORY: {proba:.1%}")
            st.progress(proba)
        else:
            st.error(f"BLUE TEAM DEFEAT: {proba:.1%}")
            st.progress(proba)
            
        st.caption(f"INPUTS: Gold Diff: {data['gold_diff_15min']} | Dragons: {data['blue_dragons']}")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center style='font-family: Roboto Mono; color: #666; font-size: 12px;'>POWERED BY RIOT GAMES DATA • DEVELOPED FOR ACADEMIC PURPOSES</center>", unsafe_allow_html=True)
