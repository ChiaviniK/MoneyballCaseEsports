import streamlit as st
import pandas as pd
import requests
import json
import time

# --- Configuração da Página (Layout Profissional) ---
st.set_page_config(
    page_title="ProScout Analytics Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILO CSS MINIMALISTA & PROFISSIONAL ---
st.markdown("""
<style>
    /* --- Configurações Globais --- */
    .stApp {
        background-color: #f8f9fa; /* Fundo Cinza Claro (Clean) */
        color: #212529; /* Texto Escuro Suave */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* --- Tipografia --- */
    h1, h2, h3 {
        font-weight: 700;
        color: #1a1a1a !important;
        letter-spacing: -0.5px;
    }
    .stCaption {
        color: #6c757d; /* Cinza médio para legendas */
        font-weight: 400;
    }
    
    /* --- Botões Modernos (Estilo SaaS) --- */
    .stButton>button {
        background-color: #0068c9; /* Azul Profissional */
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        transition: all 0.2s ease-in-out;
        height: auto;
    }
    .stButton>button:hover {
        background-color: #0053a0; /* Azul um pouco mais escuro no hover */
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
        transform: translateY(-1px);
    }
    
    /* --- Cards e Métricas Clean --- */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e9ecef; /* Borda sutil */
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03); /* Sombra muito leve */
    }
    div[data-testid="stMetricLabel"] {
        font-weight: 500;
        color: #495057;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        font-weight: 800;
        color: #0068c9; /* Azul no valor para destaque */
        font-size: 1.8rem !important;
    }
    
    /* --- Inputs Profissionais --- */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #ced4da;
        color: #495057;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0068c9;
        box-shadow: 0 0 0 2px rgba(0,104,201,0.2);
    }

    /* --- Expander Clean --- */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        font-weight: 600;
    }
    
    /* --- Área de Código (JSON View) --- */
    .stCode {
        border-radius: 8px;
        border: 1px solid #e9ecef;
        background-color: #f4f6f9 !important;
    }
    
    /* --- Ajuste da Imagem do Logo --- */
    [data-testid="stImage"] > img {
        filter: grayscale(20%); /* Deixa o logo do LoL um pouco menos "gritante" */
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Profissional ---
with st.sidebar:
    st.title("ProScout 📊")
    st.markdown("Ferramenta de análise de dados para E-sports competitivos.")
    st.markdown("---")
    st.caption("Versão: 2.1.0 (Stable)")
    st.caption("Conexão API: Riot Games (v5)")

# --- Header da Aplicação ---
col_logo, col_title = st.columns([0.5, 5])
with col_logo:
    # Ícone mais neutro ou o logo do LoL mais sóbrio
    st.image("https://img.icons8.com/color/96/league-of-legends.png", width=60)
with col_title:
    st.title("Match Intelligence Dashboard")
    st.caption("Monitoramento de partidas em tempo real e ingestão de dados via API Oficial.")

st.markdown("---")

# --- Seção 1: Ingestão de Dados Reais ---
st.subheader("📡 Conexão com API Oficial (Ingestion Pipeline)")

# Usando um container para agrupar visualmente
with st.container():
    with st.expander("🛠️ Configurações da API & Parâmetros de Busca", expanded=True):
        col_api1, col_api2, col_api3 = st.columns([2, 1, 2])
        with col_api1:
            api_key = st.text_input("Riot Developer Key (RGAPI-...)")
        with col_api2:
            region = st.selectbox("Região do Servidor", ["BR1 (Brasil)", "NA1 (América do Norte)", "KR (Coréia)"])
        with col_api3:
            summoner_name = st.text_input("Riot ID do Pro Player (Ex: Faker#KR1)")

        st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
        
        if st.button("▶️ Executar Pipeline de Coleta"):
            if not api_key or not summoner_name:
                st.warning("⚠️ Por favor, preencha a API Key e o Riot ID para iniciar a coleta.")
            else:
                with st.spinner("Autenticando na Riot Games API e buscando última partida..."):
                    # --- Simulação do Backend dos Alunos ---
                    time.sleep(2) 
                    st.toast("Dados recebidos com sucesso!", icon="✅")
                    
                    st.markdown("### 📋 Resultado da Última Partida (Live Tracker)")
                    
                    # Métricas Clean
                    cm1, cm2, cm3, cm4 = st.columns(4)
                    cm1.metric("Tipo de Fila", "Ranked Challenger")
                    cm2.metric("KDA (Performance)", "12 / 4 / 8", delta="High Impact")
                    cm3.metric("Dano Total", "42.5k")
                    cm4.metric("Desfecho", "VITÓRIA", delta_color="normal") # Cor normal (azul/verde) em vez de vermelho
                    
                    # Visualização do JSON Profissional
                    st.markdown("#### 💾 Payload Bruto (JSON Data Structure)")
                    st.caption("Estrutura de dados recebida do endpoint `/lol/match/v5/matches/{matchId}`")
                    st.code("""
{
  "metadata": {
    "matchId": "BR1_28472910_PRO",
    "dataVersion": "5.1",
    "region": "BR1"
  },
  "info": {
    "gameCreation": 1704567890123,
    "gameDuration": 1845,
    "gameMode": "CLASSIC",
    "participants": [
      {
        "summonerName": "ProPlayer_01",
        "championName": "Yasuo",
        "kills": 12, "deaths": 4, "assists": 8,
        "totalDamageDealtToChampions": 42500,
        "win": true,
        "lane": "MIDDLE"
      },
      {
        "championName": "Yone", "kills": 5, "deaths": 10, "assists": 2, "win": false
      }
      // ... mais 8 participantes
    ]
  }
}
                    """, language="json")

st.markdown("---")

# --- Seção 2: Área de Modelagem (Desafio) ---
st.subheader("🧠 Área de Modelagem Preditiva")
st.caption("Carregue dados históricos processados para alimentar o modelo de Machine Learning.")

col_upload, col_stats = st.columns([2, 1.5])

with col_upload:
    st.file_uploader("Upload de Dataset Processado (.json ou .csv)", type=["json", "csv"])
    st.caption("Formatos aceitos: JSON estruturado ou CSV normalizado conforme documentação técnica.")

with col_stats:
    # Um card visual para mostrar status do modelo
    st.markdown("""
    <div style="background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e9ecef;">
        <h4 style="margin-top:0;">Status do Modelo (Win Prediction)</h4>
        <p><strong>Engine:</strong> Python scikit-learn (Logistic Regression)</p>
        <p><strong>Acurácia Atual:</strong> <span style="color:#0068c9; font-weight:bold;">87.5%</span></p>
        <p style="font-size: 0.9rem; color: #666;">Base de treino: 15.000 partidas (Patch 14.1)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<center><small style='color: #888;'>ProScout Analytics © 2024 | Powered by Riot Games Data API | Enterprise License</small></center>", unsafe_allow_html=True)
