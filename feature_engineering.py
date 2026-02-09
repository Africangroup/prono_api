import pandas as pd

# Charger données propres
df = pd.read_csv("data/clean/matches_clean.csv")

# Trier par date
df = df.sort_values("Date")

# Fonctions utilitaires
def rolling_mean(team, column, window=5):
    return (
        df[df["HomeTeam"] == team][column]
        .rolling(window)
        .mean()
        .shift(1)
        .iloc[-1]
    )

features = []

for _, row in df.iterrows():
    home = row["HomeTeam"]
    away = row["AwayTeam"]

    feature_row = {
        "date": row["Date"],
        "home_team": home,
        "away_team": away,

        # Signaux simples mais puissants
        "home_avg_goals": rolling_mean(home, "FTHG"),
        "away_avg_goals": rolling_mean(away, "FTAG"),
        "home_goal_variance": rolling_mean(home, "total_goals"),
        "away_goal_variance": rolling_mean(away, "total_goals"),

        # Targets
        "over_1_5": int(row["total_goals"] >= 2),
        "under_3_5": int(row["total_goals"] <= 3),
    }

    features.append(feature_row)

features_df = pd.DataFrame(features)

# Nettoyage final
features_df = features_df.dropna()

# Sauvegarde
features_df.to_csv(
    "data/features/prematch_features.csv",
    index=False
)

print("✅ Feature engineering terminé")
print(features_df.head())
