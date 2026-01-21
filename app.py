import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- Configuração ---
st.set_page_config(page_title="Fut.Analytica Pro", page_icon="⚽", layout="wide")

# --- CSS Personalizado ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    h1 { color: #1e3a8a; } /* Azul Profissional */
    div[data-testid="stMetric"] {
        background-color: white; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- MAPA DE LIGAS (O Dicionário do Aluno) ---
# O aluno aprende que o usuário vê "Nome", mas o sistema usa "Código"
LIGAS = {
    "Brasileirão Série A": "BSA",
    "Premier League (Inglaterra)": "PL",
    "Champions League (Europa)": "CL",
    "La Liga (Espanha)": "PD",
    "Serie A (Itália)": "SA",
    "Bundesliga (Alemanha)": "BL1",
    "Ligue 1 (França)": "FL1"
}

# --- FUNÇÃO DE DADOS (Com Parâmetros Dinâmicos) ---
@st.cache_data
def get_football_data(api_key, league_code, season_year):
    """
    Busca dados dinâmicos baseados na escolha do usuário.
    URL muda conforme a liga e o ano.
    """
    # Construção da URL Dinâmica (f-string)
    url = f"https://api.football-data.org/v4/competitions/{league_code}/standings?season={season_year}"
    headers = {'X-Auth-Token': api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            # Tratamento especial para Champions League (que tem grupos)
            # Para simplificar para Junior, pegamos apenas a tabela TOTAL se disponível
            # ou o primeiro grupo disponível
            if 'standings' not in data or len(data['standings']) == 0:
                return pd.DataFrame()

            # Pega a primeira tabela disponível (Geral ou Grupo A)
            tabela = data['standings'][0]['table']
            
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
                    'Gols Pró': time['goalsFor'],
                    'Gols Contra': time['goalsAgainst'],
                    'Saldo Gols': time['goalDifference']
                })
            return pd.DataFrame(dados_limpos)
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- DADOS DEMO (Fallback) ---
def get_demo_data():
    return pd.DataFrame({
        'Posição': [1, 2, 3, 4, 5],
        'Time': ['Manchester City (Demo)', 'Arsenal', 'Liverpool', 'Aston Villa', 'Tottenham'],
        'Pontos': [88, 86, 80, 75, 70],
        'Gols Pró': [90, 85, 80, 70, 65],
        'Gols Contra': [30, 28, 35, 40, 45],
        'Saldo Gols': [60, 57, 45, 30, 20]
    })

# --- SIDEBAR (CONTROLES) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/soccer-ball.png", width=70)
    st.title("Fut.Analytica")
    st.caption("Agência de Scouting Esportivo")
    st.markdown("---")
    
    # 1. Input da Chave
    api_key = st.text_input("🔑 Sua API Key:", type="password")
    
    st.markdown("---")
    
    # 2. Seleção de Campeonato (Chave do Dicionário)
    nome_liga = st.selectbox("🏆 Campeonato:", list(LIGAS.keys()))
    codigo_liga = LIGAS[nome_liga] # Pega o código (ex: 'PL')
    
    # 3. Seleção de Temporada
    # A API gratuita tem limites históricos, então focamos em anos recentes
    ano = st.selectbox("📅 Temporada:", [2024, 2023, 2022])
    
    st.info(f"Buscando: {codigo_liga} / {ano}")

# --- LÓGICA PRINCIPAL ---
st.title(f"ANÁLISE: {nome_liga.upper()}")

# Carrega Dados
if api_key:
    with st.spinner("Consultando dados oficiais..."):
        df = get_football_data(api_key, codigo_liga, ano)
        
    if df.empty:
        st.warning(f"Não foram encontrados dados para {ano} ou a API Key atingiu o limite.")
        st.info("Carregando modo de demonstração...")
        df = get_demo_data()
    else:
        st.toast("Dados carregados com sucesso!", icon="✅")
else:
    st.info("Insira a API Key para ver dados reais. Mostrando demonstração.")
    df = get_demo_data()

# --- DASHBOARD JUNIOR ---

if not df.empty:
    # 1. TOP 3 (PODIUM)
    col1, col2, col3 = st.columns(3)
    
    try:
        campeao = df.iloc[0]
        vice = df.iloc[1]
        terceiro = df.iloc[2]
        
        col1.metric("🥇 Campeão/Líder", campeao['Time'], f"{campeao['Pontos']} pts")
        col2.metric("🥈 Vice-Líder", vice['Time'], f"{vice['Pontos']} pts")
        col3.metric("🥉 3º Lugar", terceiro['Time'], f"{terceiro['Pontos']} pts")
    except:
        st.write("Dados insuficientes para pódio.")

    st.markdown("---")

    # 2. GRÁFICO (SCATTER PLOT)
    st.subheader("🎯 Eficiência Ofensiva x Defensiva")
    
    tab1, tab2 = st.tabs(["Gráfico de Dispersão", "Tabela Completa"])
    
    with tab1:
        # Gráfico colorido e interativo
        fig = px.scatter(
            df,
            x="Gols Pró",
            y="Gols Contra",
            text="Time",
            size="Pontos",
            color="Posição",
            color_continuous_scale="bluered", # Azul (Topo) -> Vermelho (Baixo)
            title=f"Performance dos Clubes: {ano}"
        )
        # Inverte o eixo Y (porque levar MENOS gols é melhor, então deve ficar no topo visualmente ou explicamos o gráfico)
        # Vamos manter padrão: Quanto mais pra direita (mais gols) e mais pra baixo (menos gols sofridos), melhor.
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Dica de Análise: Os melhores times ficam no canto **Inferior Direito** (Muitos Gols Feitos, Poucos Sofridos).")

    with tab2:
        st.dataframe(df, use_container_width=True, hide_index=True)

    # 3. EXPORTAÇÃO
    st.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Relatório (Excel/CSV)", csv, f"dados_{codigo_liga}_{ano}.csv", "text/csv")
