import pandas as pd

# Charger la dernière situation analysée
df = pd.read_csv("data/live_training.csv")
row = df.tail(1).iloc[0]

print("\n🧠 APPRENTISSAGE DU BOT")
print("1 = BUT arrivé après le signal")
print("0 = PAS de but")

result = int(input("👉 Résultat réel : "))

data = {
    "minute": int(row["minute"]),
    "proba": float(row["proba_goal"]),
    "xg": float(row["xg_total"]),
    "shots": int(row["shots_total"]),
    "fouls": int(row["fouls_total"]),
    "result": result
}

memory = pd.read_csv("memory.csv")
memory = pd.concat([memory, pd.DataFrame([data])], ignore_index=True)
memory.to_csv("memory.csv", index=False)

print("✅ Le bot a appris de ce match")
