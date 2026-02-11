from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI(title="VrSOCCER API", version="1.0")

model = joblib.load("models/live_xgb.pkl")

@app.get("/")
def home():
    return {"status": "API VrSOCCER ACTIVE"}

@app.get("/predict")
def predict():
    df = pd.read_csv("data/live_training.csv")

@app.get("/prematch/analyze")
def prematch_test():
    return {
        "status": "PREMATCH OK",
        "message": "Endpoint prematch actif"
    }

    if df.empty:
        return {"error": "Aucune donnée LIVE"}

    row = df.iloc[-1]

    X = pd.DataFrame([{
        "minute": row["minute"],
        "goals_total": row["goals_total"],
        "shots_total": row["shots_total"],
        "xg_total": row["xg_total"],
        "fouls_total": row["fouls_total"]
    }])

    proba = float(model.predict_proba(X)[0][1])

    decision = (
        row["minute"] >= 60 and
        proba >= 0.65 and
        row["shots_total"] >= 12 and
        row["xg_total"] >= 1.5 and
        row["fouls_total"] <= 22
    )

    return {
        "minute": int(row["minute"]),
        "probability": round(proba, 2),
        "shots": int(row["shots_total"]),
        "xg": round(row["xg_total"], 2),
        "fouls": int(row["fouls_total"]),
        "bet_allowed": decision
    }

