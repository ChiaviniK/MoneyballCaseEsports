import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib # Para salvar o modelo

print(">>> INICIANDO TREINAMENTO DO ORÁCULO (ML)...")

# 1. Simular um Dataset Histórico (Já que não temos os dados da Riot agora)
# Em um cenário real, isso viria do SQL.
n_samples = 5000
data = {
    'gold_diff_15min': np.random.normal(0, 2000, n_samples), # Diferença de ouro
    'blue_dragons': np.random.randint(0, 5, n_samples),      # Dragões do time azul
    'red_dragons': np.random.randint(0, 5, n_samples),       # Dragões do time vermelho
    'blue_tower_kills': np.random.randint(0, 11, n_samples),
    'vision_score_diff': np.random.normal(0, 20, n_samples)
}
df = pd.DataFrame(data)

# Lógica "Realista": Quem tem mais ouro e dragões tende a ganhar
df['win_prob'] = (
    (df['gold_diff_15min'] * 0.0005) + 
    (df['blue_dragons'] * 0.1) - 
    (df['red_dragons'] * 0.1) + 
    np.random.normal(0, 0.2, n_samples)
)
df['blue_win'] = (df['win_prob'] > 0).astype(int) # 0 ou 1

# 2. Preparar Features (X) e Target (y)
X = df[['gold_diff_15min', 'blue_dragons', 'red_dragons', 'vision_score_diff']]
y = df['blue_win']

# 3. Treinar Modelo (Regressão Logística)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Avaliar
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)
print(f"✅ Modelo Treinado! Acurácia no Teste: {acc:.1%}")

# 5. Salvar o "Cérebro" para usar no App
joblib.dump(model, 'lol_win_predictor.pkl')
print("💾 Modelo salvo como 'lol_win_predictor.pkl'")
