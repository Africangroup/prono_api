import pandas as pd
import joblib

# Charger données
df = pd.read_csv("data/features/prematch_features.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Charger modèle calibré
model = joblib.load("models/rf_over15_calibrated.pkl")

FEATURES = [
    "home_avg_goals",
    "away_avg_goals",
    "home_goal_variance",
    "away_goal_variance"
]

THRESHOLD = 0.75   # règle NO BET
STAKE = 1          # mise fixe

results = []

for _, row in df.iterrows():
    X = row[FEATURES].to_frame().T
    proba = model.predict_proba(X)[0][1]

    if proba < THRESHOLD:
        results.append({
            "date": row["date"],
            "decision": "NO BET",
            "profit": 0
        })
        continue

    # Pari pris
    win = row["over_1_5"] == 1
    profit = STAKE if win else -STAKE

    results.append({
        "date": row["date"],
        "decision": "BET",
        "profit": profit
    })

# Résultats globaux
results_df = pd.DataFrame(results)

total_bets = (results_df["decision"] == "BET").sum()
no_bets = (results_df["decision"] == "NO BET").sum()
profit_total = results_df["profit"].sum()

print("📊 BACKTEST TERMINÉ")
print(f"Total matchs : {len(results_df)}")
print(f"Paris pris   : {total_bets}")
print(f"NO BET       : {no_bets}")
print(f"Profit total : {profit_total}")
