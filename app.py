import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- Configuração da Página ---
st.set_page_config(
    page_title="Fut.Analytica Pro", 
    page_icon="⚽", 
    layout="wide"
)

# --- Estilização (CSS Simples) ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #1e3a8a; font-family: 'Arial Black', sans-serif; }
    div[data-testid="stMetric"] {
        background-color: white; 
        border: 1px solid #d1d5db; 
        border-radius: 8px; 
        padding: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- MAPA DE LIGAS (O Dicionário do Aluno) ---
# O sistema usa o Código (ex: 'BSA'), mas o usuário vê o Nome.
LIGAS = {
    "Brasileirão Série A": "BSA",
    "Premier League (Inglaterra)": "PL",
    "Champions League (Europa)": "CL",
    "La Liga (Espanha)": "PD",
    "Serie A (Itália)": "SA",
    "Bundesliga (Alemanha)": "BL1",
    "Ligue 1 (França)": "FL1"
}

# --- FUNÇÃO 1: BUSCAR DADOS REAIS (API) ---
@st.cache_data
def get_football_data(api_key, league_code, season_year):
    """
    Vai na internet buscar a tabela atualizada.
    """
    url = f"https://api.football-data.org/v4/competitions/{league_code}/standings?season={season_year}"
    headers = {'X-Auth-Token': api_key}
    
    try:
        response = requests.get(url, headers=headers)
        
        # Se a resposta for "OK" (200)
        if response.status_code == 200:
            data = response.json()
            
            # Verifica se existe tabela para esse ano
            if 'standings' not in data or len(data['standings']) == 0:
                return pd.DataFrame() # Retorna vazio se não tiver dados

            # Pega a primeira tabela (Geral ou Grupo A)
            tabela = data['standings'][0]['table']
            
            # ETL: Transformando o JSON bagunçado em Tabela limpa
            dados_limpos = []
            for time in tabela:
                dados_limpos.append({
                    'Posição': time['position'],
                    'Time': time['team']['name'],
                    'Pontos': time['points'],
                    'Jogos': time['playedGames'],
                    'Vitórias': time['won'],
                    'Derrotas': time['lost'],
                    'Empates': time['draw'],
                    'Gols Pró': time['goalsFor'],     # Ataque
                    'Gols Contra': time['goalsAgainst'], # Defesa
                    'Saldo Gols': time['goalDifference']
                })
            return pd.DataFrame(dados_limpos)
        else:
            return pd.DataFrame() # Erro na API (403, 429, etc)
    except:
        return pd.DataFrame() # Erro de conexão

# --- FUNÇÃO 2: DADOS DE EXEMPLO (DEMO) ---
def get_demo_data():
    """Gera dados fictícios para a aula não parar se a API falhar."""
    return pd.DataFrame({
        'Posição': [1, 2, 3, 4, 5],
        'Time': ['Real Madrid', 'Manchester City', 'Bayern Munich', 'Arsenal', 'Inter Milan'],
        'Pontos': [45, 43, 40, 39, 38],
        'Jogos': [19, 19, 19, 19, 19],
        'Vitórias': [14, 13, 12, 11, 11],
        'Gols Pró': [42, 40, 45, 35, 30],
        'Gols Contra': [15, 18, 20, 12, 10],
        'Saldo Gols': [27, 22, 25, 23, 20]
    })

# --- SIDEBAR (Barra Lateral) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/soccer-ball.png", width=80)
    st.title("Fut.Analytica")
    st.caption("Sistema de Scouting Esportivo")
    st.markdown("---")
    
    # 1. API Key
    api_key = st.text_input("🔑 Sua API Key (Opcional):", type="password")
    if not api_key:
        st.info("Sem chave? Usaremos o Modo Demo.")
    
    st.markdown("---")
    
    # 2. Seletores
    nome_liga = st.selectbox("🏆 Campeonato:", list(LIGAS.keys()))
    codigo_liga = LIGAS[nome_liga] # Traduz o nome para código (ex: 'BSA')
    
    # Seletor de Ano (Com lógica pedagógica)
    ano = st.selectbox(
        "📅 Temporada (Ano de Início):", 
        [2025, 2024, 2023, 2026],
        index=0, # Padrão: 2025 (Temporada Ativa na Europa)
        help="Na Europa, a temporada que acaba em 2026 chama-se '2025'."
    )
    
    # Aviso de Integridade de Dados
    if ano == 2026 and codigo_liga == "BSA":
        st.warning("⚠️ O Brasileirão 2026 começa apenas em Abril! Tabela vazia.")

# --- LÓGICA PRINCIPAL ---
st.title(f"RAIO-X: {nome_liga.upper()} ({ano})")

# Carregamento dos Dados
if api_key:
    with st.spinner(f"Baixando dados da {nome_liga}..."):
        df = get_football_data(api_key, codigo_liga, ano)
        
    if df.empty:
        if ano == 2026:
            st.warning("📅 Campeonato ainda não começou ou sem dados disponíveis.")
        else:
            st.error("Erro na API ou Chave Inválida. Carregando dados de exemplo...")
            df = get_demo_data()
    else:
        st.toast("Dados Oficiais Carregados!", icon="✅")
else:
    # Se não tiver chave, carrega demo direto
    df = get_demo_data()
    st.info("👀 Visualizando dados de DEMONSTRAÇÃO.")

# --- DASHBOARD ---

if not df.empty:
    # 1. PÓDIO (Métricas)
    st.subheader("🏆 O Pódio")
    col1, col2, col3 = st.columns(3)
    
    try:
        # Tenta pegar os 3 primeiros. Se o campeonato acabou de começar, pode ter menos.
        if len(df) >= 1:
            col1.metric("🥇 Líder", df.iloc[0]['Time'], f"{df.iloc[0]['Pontos']} pts")
        if len(df) >= 2:
            col2.metric("🥈 Vice-Líder", df.iloc[1]['Time'], f"{df.iloc[1]['Pontos']} pts")
        if len(df) >= 3:
            col3.metric("🥉 3º Lugar", df.iloc[2]['Time'], f"{df.iloc[2]['Pontos']} pts")
    except:
        st.write("Aguardando mais jogos para definir o pódio.")

    st.markdown("---")

    # 2. GRÁFICO (Scatter Plot)
    st.subheader("📊 Análise de Eficiência")
    st.caption("Dica: Times no **canto inferior direito** são os melhores (Fazem muito gol e levam pouco).")
    
    tab1, tab2 = st.tabs(["Gráfico Visual", "Tabela de Dados"])
    
    with tab1:
        fig = px.scatter(
            df,
            x="Gols Pró",
            y="Gols Contra",
            text="Time",
            size="Pontos",
            color="Saldo Gols",
            color_continuous_scale="RdYlGn", # Vermelho -> Amarelo -> Verde
            title=f"Ataque vs Defesa ({ano})",
            labels={"Gols Pró": "Gols Marcados (Ataque)", "Gols Contra": "Gols Sofridos (Defesa)"}
        )
        # Ajuste visual para o texto não ficar em cima da bolinha
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.dataframe(
            df[['Posição', 'Time', 'Pontos', 'Jogos', 'Vitórias', 'Saldo Gols']],
            hide_index=True,
            use_container_width=True
        )

    # 3. DOWNLOAD
    st.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Relatório (CSV)",
        data=csv,
        file_name=f"tabela_{codigo_liga}_{ano}.csv",
        mime="text/csv"
    )
