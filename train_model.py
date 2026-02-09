import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Charger les features
df = pd.read_csv("data/features/prematch_features.csv")

# Trier par date (CRUCIAL)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Séparation temporelle (80% train / 20% test)
split_index = int(len(df) * 0.8)
train = df.iloc[:split_index]
test = df.iloc[split_index:]

# Features utilisées
FEATURES = [
    "home_avg_goals",
    "away_avg_goals",
    "home_goal_variance",
    "away_goal_variance"
]

TARGET = "over_1_5"

X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]

# Modèle volontairement bridé
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=6,
    min_samples_leaf=50,
    class_weight="balanced",
    random_state=42
)

# Entraînement
model.fit(X_train, y_train)

# Évaluation
preds = model.predict(X_test)
print("📊 RAPPORT DE CLASSIFICATION")
print(classification_report(y_test, preds))

# Sauvegarde
joblib.dump(model, "models/rf_over15.pkl")
print("✅ Modèle sauvegardé")
