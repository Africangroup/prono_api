import os
import pandas as pd
from xgboost import XGBClassifier
import joblib

# Crée le dossier si nécessaire
os.makedirs("data/models", exist_ok=True)

# Exemple de jeu de données minimal
X = pd.DataFrame({
    'minute': [10, 20, 30, 40, 50],
    'goals_total': [0, 1, 0, 1, 0],
    'shots_total': [2, 3, 1, 4, 2],
    'xg_total': [0.1, 0.3, 0.2, 0.5, 0.2],
    'fouls_total': [1, 2, 0, 3, 1]
})
y = [0, 1, 0, 1, 0]

# Entraîne le modèle
model = XGBClassifier()
model.fit(X, y)

# Sauvegarde le modèle
joblib.dump(model, "data/models/live_xgb.pkl")
print("✅ Modèle créé et sauvegardé dans data/models/live_xgb.pkl")
