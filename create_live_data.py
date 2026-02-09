import pandas as pd
import os

os.makedirs("data", exist_ok=True)

df = pd.DataFrame([{
    "minute": 65,
    "goals_total": 1,
    "shots_total": 12,
    "xg_total": 1.4,
    "fouls_total": 18,
    "proba_goal": 0.62
}])

df.to_csv("data/live_training.csv", index=False)
print("✅ Ligne LIVE test créée")
