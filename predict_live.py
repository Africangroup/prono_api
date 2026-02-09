import pandas as pd
import joblib

# 🔥 LIRE LE BON FICHIER
df = pd.read_csv("data/live_prepared.csv")

# Charger le modèle
model = joblib.load("models/live_goal_model.pkl")

# Dernière ligne LIVE
live = df[
    [
        "minute",
        "goals_total",
        "shots_total",
        "xg_total",
        "fouls_total"
    ]
].tail(1)

# Prédiction
proba = model.predict_proba(live)[0][1]

print(f"⚽ Probabilité de BUT prochainement : {proba:.2f}")

if proba >= 0.65:
    print("🔥 SIGNAL FORT")
elif proba >= 0.55:
    print("⚠️ Signal moyen")
else:
    print("❌ Pas de bet")









