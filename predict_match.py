import pandas as pd
import joblib

# Charger modèle calibré
model = joblib.load("models/rf_over15_calibrated.pkl")

FEATURES = [
    "home_avg_goals",
    "away_avg_goals",
    "home_goal_variance",
    "away_goal_variance"
]

# Exemple de match (à remplacer plus tard par données live)
match = pd.DataFrame([{
    "home_avg_goals": 1.4,
    "away_avg_goals": 1.2,
    "home_goal_variance": 2.6,
    "away_goal_variance": 2.4
}])

proba = model.predict_proba(match)[0][1]

print(f"📈 Probabilité Over 1.5 : {proba:.2f}")

# RÈGLE NO BET
if proba >= 0.75:
    print("✅ BET AUTORISÉ")
else:
    print("❌ NO BET")
