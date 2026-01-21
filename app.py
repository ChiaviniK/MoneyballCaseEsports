import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Fut.Analytica Pro", page_icon="⚽", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #1e3a8a; }
    div[data-testid="stMetric"] { background-color: white; border-radius: 8px; padding: 10px; border: 1px solid #d1d5db; }
</style>
""", unsafe_allow_html=True)

LIGAS = {
    "Brasileirão Série A": "BSA",
    "Premier League (Inglaterra)": "PL",
    "Champions League (Europa)": "CL",
    "La Liga (Espanha)": "PD",
    "Serie A (Itália)": "SA",
    "Bundesliga (Alemanha)": "BL1",
    "Ligue 1 (França)": "FL1"
}

# --- FUNÇÃO 1: TABELA (JÁ EXISTIA) ---
@st.cache_data
def get_football_data(api_key, league_code, season_year):
    url = f"https://api.football-data.org/v4/competitions/{league_code}/standings?season={season_year}"
    headers = {'X-Auth-Token': api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'standings' not in data or len(data['standings']) == 0: return pd.DataFrame()
            tabela = data['standings'][0]['table']
            dados = []
            for time in tabela:
                dados.append({
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
            return pd.DataFrame(dados)
        return pd.DataFrame()
    except: return pd.DataFrame()

# --- FUNÇÃO 2: ARTILHEIROS (NOVIDADE!) ---
@st.cache_data
def get_top_scorers(api_key, league_code, season_year):
    """Busca a lista de artilheiros da competição."""
    url = f"https://api.football-data.org/v4/competitions/{league_code}/scorers?season={season_year}"
    headers = {'X-Auth-Token': api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            scorers = data['scorers']
            
            dados = []
            for player in scorers:
                dados.append({
                    'Jogador': player['player']['name'],
                    'Time': player['team']['name'],
                    'Gols': player['goals'],
                    # A API free as vezes manda assistencias como None, mas tentamos pegar
                    'Assistências': player.get('assists') or 0, 
                    'Penaltis': player.get('penalties') or 0
                })
            return pd.DataFrame(dados)
        return pd.DataFrame()
    except: return pd.DataFrame()

# --- DADOS DEMO (TABELA) ---
def get_demo_data():
    return pd.DataFrame({
        'Posição': [1, 2, 3, 4, 5],
        'Time': ['Real Madrid', 'Man City', 'Bayern', 'Arsenal', 'Inter'],
        'Pontos': [45, 43, 40, 39, 38],
        'Jogos': [19, 19, 19, 19, 19],
        'Vitórias': [14, 13, 12, 11, 11],
        'Gols Pró': [42, 40, 45, 35, 30],
        'Gols Contra': [15, 18, 20, 12, 10],
        'Saldo Gols': [27, 22, 25, 23, 20]
    })

# --- DADOS DEMO (ARTILHEIROS) ---
def get_demo_scorers():
    return pd.DataFrame({
        'Jogador': ['Haaland', 'Mbappé', 'Kane', 'Salah', 'Vinicius Jr'],
        'Time': ['Man City', 'Real Madrid', 'Bayern', 'Liverpool', 'Real Madrid'],
        'Gols': [18, 16, 15, 14, 12],
        'Assistências': [2, 5, 4, 8, 7],
        'Penaltis': [3, 2, 4, 1, 0]
    })

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/soccer-ball.png", width=80)
    st.title("Fut.Analytica")
    st.markdown("---")
    api_key = st.text_input("🔑 API Key:", type="password")
    if not api_key: st.info("Modo Demo Ativo")
    st.markdown("---")
    nome_liga = st.selectbox("🏆 Campeonato:", list(LIGAS.keys()))
    codigo_liga = LIGAS[nome_liga]
    ano = st.selectbox("📅 Temporada:", [2025, 2024, 2023, 2026], index=0)
    if ano == 2026 and codigo_liga == "BSA": st.warning("Camp. Brasileiro 2026 não começou.")

# --- MAIN ---
st.title(f"RAIO-X: {nome_liga.upper()} ({ano})")

if api_key:
    # Busca os dois dados!
    with st.spinner("Analisando estatísticas..."):
        df = get_football_data(api_key, codigo_liga, ano)
        df_scorers = get_top_scorers(api_key, codigo_liga, ano)
    
    if df.empty:
        if ano != 2026:
            st.error("Erro na API. Usando Demo.")
            df = get_demo_data()
            df_scorers = get_demo_scorers()
else:
    df = get_demo_data()
    df_scorers = get_demo_scorers()

# --- DASHBOARD ---
if not df.empty:
    
    # CRIAÇÃO DE ABAS (AQUI ESTÁ A MÁGICA)
    tab_class, tab_artilharia, tab_analise = st.tabs(["📋 Classificação", "⚽ Artilharia (Gols)", "📊 Gráficos"])
    
    with tab_class:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(df[['Posição', 'Time', 'Pontos', 'Jogos', 'Vitórias', 'Saldo Gols']], hide_index=True, use_container_width=True)
        with col2:
            st.subheader("Líder")
            lider = df.iloc[0]
            st.metric("Time", lider['Time'])
            st.metric("Aproveitamento", f"{(lider['Pontos']/(lider['Jogos']*3))*100:.1f}%")

    with tab_artilharia:
        if not df_scorers.empty:
            st.subheader(f"Chuteira de Ouro {ano}")
            
            # Gráfico de Barras Horizontal dos Artilheiros
            fig_goals = px.bar(
                df_scorers.head(10).sort_values('Gols', ascending=True), 
                x='Gols', 
                y='Jogador', 
                orientation='h',
                text='Gols',
                color='Time',
                title="Top 10 Artilheiros"
            )
            st.plotly_chart(fig_goals, use_container_width=True)
            
            st.dataframe(df_scorers, hide_index=True, use_container_width=True)
        else:
            st.warning("Dados de artilharia indisponíveis para esta liga/ano na versão Free.")

    with tab_analise:
        st.subheader("Eficiência: Ataque x Defesa")
        fig = px.scatter(
            df, x="Gols Pró", y="Gols Contra", text="Time", size="Pontos",
            color="Saldo Gols", color_continuous_scale="RdYlGn",
            title=f"Mapa de Performance ({ano})"
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

    # DOWNLOAD UNIFICADO
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.download_button("📥 Baixar Tabela (CSV)", df.to_csv(index=False).encode('utf-8'), "tabela.csv", "text/csv")
    if not df_scorers.empty:
        c2.download_button("📥 Baixar Artilheiros (CSV)", df_scorers.to_csv(index=False).encode('utf-8'), "gols.csv", "text/csv")
