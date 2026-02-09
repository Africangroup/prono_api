import pandas as pd


# Charger les données
df = pd.read_csv("data/matches.csv")

# Créer les colonnes TOTAL
df["goals_total"] = df["goals_home"] + df["goals_away"]
df["shots_total"] = df["shots_home"] + df["shots_away"]
df["xg_total"] = df["xg_home"] + df["xg_away"]
df["fouls_total"] = df["fouls_home"] + df["fouls_away"]

# Créer la TARGET (but dans les prochaines minutes)
df["target"] = (df["goals_total"].diff().fillna(0) > 0).astype(int)

# Sauvegarde
df.to_csv("data/live_prepared.csv", index=False)

print("✅ Données LIVE préparées avec colonnes TOTAL + TARGET")

# Charger données live brutes
df = pd.read_csv("data/matches.csv")

# Trier par match et minute
df = df.sort_values(["match_id", "minute"])

# Calculs sur 5 minutes glissantes
df["shots_5min"] = (
    df.groupby("match_id")["shots_home"]
    .diff()
    .rolling(5)
    .sum()
)

df["xg_5min"] = (
    df.groupby("match_id")["xg_home"]
    .diff()
    .rolling(5)
    .sum()
)

df["fouls_5min"] = (
    df.groupby("match_id")["fouls_home"]
    .diff()
    .rolling(5)
    .sum()
)

# Index de pression simple
df["pressure_index"] = (
    df["shots_5min"].fillna(0) * 0.5 +
    df["xg_5min"].fillna(0) * 2 +
    df["fouls_5min"].fillna(0) * 0.3
)

# CIBLE : but dans les minutes suivantes
df["target"] = (
    (df["goals_home"].shift(-1) > df["goals_home"])
).astype(int)

# Garder colonnes utiles
features = [
    "minute",
    "shots_5min",
    "xg_5min",
    "fouls_5min",
    "pressure_index",
    "target"
]

df_live = df[features].dropna()

df_live.to_csv("data/live_training.csv", index=False)

print("✅ Données LIVE avec pression 5 minutes créées")
