import pandas as pd

# 1️⃣ Charger la dernière prédiction LIVE
df = pd.read_csv("data/live_training.csv")

# On prend la dernière ligne (match en cours)
row = df.tail(1)

# 2️⃣ Paramètres (TU PEUX CHANGER LA COTE)
prob_model = row["proba_goal"].values[0] if "proba_goal" in row else 0.57
book_odds = 2.10  # 👈 COTE BOOKMAKER

# 3️⃣ Calculs
prob_book = 1 / book_odds
value = prob_model - prob_book

# 4️⃣ Décision
print(f"📊 Proba modèle : {prob_model:.2f}")
print(f"📊 Proba bookmaker : {prob_book:.2f}")
print(f"📈 Value : {value:.2%}")

if value > 0.08:
    print("🔥 STRONG BET – Value très élevée")
elif value > 0.04:
    print("⚠️ SMALL BET – Value correcte")
else:
    print("❌ NO BET – Aucun avantage")
