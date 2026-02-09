from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI()

model = joblib.load("data/models/live_xgb.pkl")

@app.get("/")
def home():
    return {"status": "API PRONO ACTIVE"}

@app.get("/signal")
def signal():
    df = pd.read_csv("data/live_training.csv")
    row = df.tail(1)

    X = row[[
        "minute",
        "goals_total",
        "shots_total",
        "xg_total",
        "fouls_total"
    ]]

    proba = float(model.predict_proba(X)[0][1])
    minute = int(row["minute"].values[0])

    decision = bool(
        proba >= 0.60 and minute >= 60
    )

    return {
        "minute": minute,
        "proba_goal": round(proba, 2),
        "bet": decision
    }
