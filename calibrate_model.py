import pandas as pd
import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import TimeSeriesSplit

# Charger les données
df = pd.read_csv("data/features/prematch_features.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

FEATURES = [
    "home_avg_goals",
    "away_avg_goals",
    "home_goal_variance",
    "away_goal_variance"
]

TARGET = "over_1_5"

X = df[FEATURES]
y = df[TARGET]

# Charger le modèle existant
base_model = joblib.load("models/rf_over15.pkl")

# Calibration temporelle
calibrator = CalibratedClassifierCV(
    base_model,
    method="isotonic",
    cv=TimeSeriesSplit(n_splits=5)
)

calibrator.fit(X, y)

# Sauvegarde
joblib.dump(calibrator, "models/rf_over15_calibrated.pkl")

print("✅ Modèle calibré sauvegardé")
