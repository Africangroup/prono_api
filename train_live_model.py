import pandas as pd
from xgboost import XGBClassifier
import joblib

# 🔥 LIRE LE BON FICHIER
df = pd.read_csv("data/live_prepared.csv")

# Colonnes utilisées par le modèle
X = df[
    [
        "minute",
        "goals_total",
        "shots_total",
        "xg_total",
        "fouls_total"
    ]
]

y = df["target"]

# Modèle
model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    eval_metric="logloss"
)

model.fit(X, y)

# Sauvegarde
joblib.dump(model, "models/live_goal_model.pkl")

print("💾 Modèle LIVE entraîné et sauvegardé correctement")
