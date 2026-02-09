import pandas as pd

# Charger les données brutes
df = pd.read_csv("data/raw/E0.csv")

# Colonnes essentielles seulement
columns_to_keep = [
    "Date",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR"
]

df = df[columns_to_keep]

# Supprimer les lignes incomplètes
df = df.dropna()

# Convertir la date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Créer des features simples
df["total_goals"] = df["FTHG"] + df["FTAG"]
df["home_win"] = (df["FTR"] == "H").astype(int)
df["away_win"] = (df["FTR"] == "A").astype(int)
df["draw"] = (df["FTR"] == "D").astype(int)

# Sauvegarde
df.to_csv("data/clean/matches_clean.csv", index=False)

print("✅ Nettoyage terminé")
print(df.head())
