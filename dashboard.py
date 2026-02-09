import pandas as pd

# Charger la mémoire des paris
df = pd.read_csv("memory.csv")

if df.empty:
    print("❌ Aucune donnée pour le moment")
    exit()

total = len(df)
wins = int(df["result"].sum())
losses = total - wins
winrate = round(wins / total * 100, 2)

# Hypothèse simple : gain = +1, perte = -1
profit = wins - losses

print("\n📊 TABLEAU DE BORD DU BOT\n")
print(f"📌 Nombre de paris : {total}")
print(f"✅ Paris gagnés   : {wins}")
print(f"❌ Paris perdus   : {losses}")
print(f"📈 Taux réussite  : {winrate}%")
print(f"💰 Profit estimé  : {profit} unités\n")
