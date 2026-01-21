import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# --- Configuração ---
st.set_page_config(page_title="Fut.Analytica ⚽", layout="wide")

# --- CSS Simples ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #2e7d32; }
    div[data-testid="stMetric"] { background-color: white; border-radius: 10px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# --- FUNÇÃO QUE PEGA DADOS REAIS ---
@st.cache_data
def get_brasileirao_data(api_key):
    """
    Busca a tabela do Brasileirão Série A (BSA).
    Documentação: https://www.football-data.org/documentation/quickstart
    """
    url = "https://api.football-data.org/v4/competitions/BSA/standings"
    headers = {'X-Auth-Token': api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # O JSON é complexo: standings -> lista -> table
            tabela = data['standings'][0]['table']
            
            # Engenharia de Dados (ETL Simples)
            # Transformando lista de dicionários em colunas limpas
            dados_limpos = []
            for time in tabela:
                dados_limpos.append({
                    'Posição': time['position'],
                    'Time': time['team']['name'],
                    'Pontos': time['points'],
                    'Jogos': time['playedGames'],
                    'Vitórias': time['won'],
                    'Empates': time['draw'],
                    'Derrotas': time['lost'],
                    'Gols Pró': time['goalsFor'],
                    'Gols Contra': time['goalsAgainst'],
                    'Saldo Gols': time['goalDifference'],
                    'Escudo': time['team']['crest']
                })
            return pd.DataFrame(dados_limpos)
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- DADOS DE EXEMPLO (Caso o aluno não tenha API Key) ---
def get_demo_data():
    return pd.DataFrame({
        'Posição': [1, 2, 3, 4, 5],
        'Time': ['Botafogo', 'Palmeiras', 'Flamengo', 'Fortaleza', 'Internacional'],
        'Pontos': [68, 64, 60, 58, 55],
        'Gols Pró': [55, 50, 48, 40, 42],
        'Gols Contra': [20, 25, 30, 28, 22],
        'Saldo Gols': [35, 25, 18, 12, 20]
    })

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/football.png", width=80)
    st.title("Fut.Analytica")
    st.markdown("---")
    
    # Input da API Key (Segurança básica)
    api_key = st.text_input("Cole sua API Key aqui:", type="password")
    st.caption("Sem chave? Usaremos dados de exemplo.")
    
    st.markdown("---")
    st.write("Fonte: football-data.org")

# --- LÓGICA PRINCIPAL ---
st.title("RAIO-X DO BRASILEIRÃO 🇧🇷")

if api_key:
    df = get_brasileirao_data(api_key)
    if df.empty:
        st.warning("Chave inválida ou erro na API. Carregando demo...")
        df = get_demo_data()
    else:
        st.toast("Dados atualizados da API!", icon="⚽")
else:
    df = get_demo_data()

# --- DASHBOARD ---

# 1. KPIs do Líder
lider = df.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Líder do Campeonato", lider['Time'])
c2.metric("Pontuação", lider['Pontos'])
c3.metric("Melhor Ataque (Gols)", df['Gols Pró'].max())
c4.metric("Melhor Defesa (Gols)", df['Gols Contra'].min())

st.markdown("---")

# 2. GRÁFICO DE DISPERSÃO (ATAQUE vs DEFESA)
st.subheader("📊 Eficiência: Ataque vs Defesa")
st.caption("Times no canto SUPERIOR DIREITO fazem muitos gols mas sofrem muitos. Times no canto INFERIOR DIREITO são equilibrados.")

fig = px.scatter(
    df, 
    x="Gols Pró", 
    y="Gols Contra", 
    text="Time", 
    size="Pontos", 
    color="Saldo Gols",
    color_continuous_scale="RdYlGn", # Vermelho (Ruim) -> Verde (Bom)
    title="Mapa de Desempenho dos Clubes"
)
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)

# 3. TABELA DETALHADA
st.subheader("📋 Classificação Oficial")

# Formatação visual da tabela (Pandas Styler)
st.dataframe(
    df[['Posição', 'Time', 'Pontos', 'Jogos', 'Vitórias', 'Saldo Gols']],
    hide_index=True,
    use_container_width=True
)

# 4. DOWNLOAD
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Baixar Tabela (CSV)", csv, "brasileirao.csv", "text/csv")
