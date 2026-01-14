import requests
import pandas as pd
import time

# --- CONFIGURAÇÃO ---
# Alunos devem pegar a chave em: https://developer.riotgames.com/
API_KEY = "RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" 
HEADERS = {"X-Riot-Token": API_KEY}

def get_puuid(game_name, tag_line):
    """Busca o ID único do jogador (PUUID)"""
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()['puuid']
    return None

def get_matches(puuid, count=5):
    """Busca os IDs das últimas partidas"""
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    resp = requests.get(url, headers=HEADERS)
    return resp.json() if resp.status_code == 200 else []

def get_match_details(match_id):
    """Busca os detalhes (kills, gold, champs) da partida"""
    url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
    resp = requests.get(url, headers=HEADERS)
    return resp.json() if resp.status_code == 200 else None

# --- FLUXO PRINCIPAL (Tarefa do Aluno) ---
print(">>> INICIANDO COLETA DE DADOS RIOT...")

# 1. Definir um jogador alvo (Ex: um Pro Player)
player = "Kami"
tag = "BR1"

puuid = get_puuid(player, tag)
if puuid:
    print(f"✅ Jogador encontrado: {puuid}")
    
    matches = get_matches(puuid, count=10)
    print(f"🎮 {len(matches)} partidas encontradas.")
    
    dados_partidas = []
    
    for m_id in matches:
        print(f"Baixando {m_id}...")
        details = get_match_details(m_id)
        if details:
            # O aluno deve escolher o que salvar. Ex:
            info = details['info']
            dados_partidas.append({
                'match_id': m_id,
                'duration': info['gameDuration'],
                'mode': info['gameMode'],
                # Desafio: Extrair dados dos 10 participantes
                'participants': info['participants'] 
            })
        time.sleep(1.2) # Respeitar Rate Limit da Riot (Importante!)

    # Salvar JSON para usar no Dashboard
    df = pd.DataFrame(dados_partidas)
    df.to_json("riot_matches_real.json", orient="records")
    print("💾 Arquivo 'riot_matches_real.json' salvo com sucesso!")
else:
    print("❌ Jogador não encontrado ou API Key expirada.")
