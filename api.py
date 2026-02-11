from fastapi import FastAPI
from core.prematch_analysis import prematch_engine
from supabase_client import supabase
import pandas as pd
import joblib

app = FastAPI(title="PRONO API", version="1.0")

# Chargement du modèle live
model = joblib.load("models/live_xgb.pkl")


# ===============================
# 🟢 ROUTE TEST
# ===============================
@app.get("/")
def home():
    return {"status": "API PRONO ACTIVE"}


# ===============================
# 🔵 RECUPERER STATS PREMATCH
# ===============================
@app.get("/prematch")
def get_prematch():
    response = supabase.table("prematch_stats").select("*").execute()
    return response.data


# ===============================
# 🔴 ANALYSE LIVE
# ===============================
@app.get("/live/signal")
def live_signal():

    df = pd.read_csv("data/live_training.csv")

    if df.empty:
        return {"error": "No live data"}

    row = df.iloc[-1]

    X = pd.DataFrame([{
        "minute": row["minute"],
        "goals_total": row["goals_total"],
        "shots_total": row["shots_total"],
        "xg_total": row["xg_total"],
        "fouls_total": row["fouls_total"]
    }])

    proba = float(model.predict_proba(X)[0][1])
    minute = int(row["minute"])

    decision = bool(proba >= 0.60 and minute >= 60)

    return {
        "type": "LIVE",
        "minute": minute,
        "confidence": round(proba * 100, 1),
        "bet": decision,
        "risk": "faible" if proba >= 0.70 else "moyen",
        "reason": "Pression offensive + xG élevé"
    }


# ===============================
# 🟣 ANALYSE PREMATCH IA
# ===============================
@app.get("/prematch/analyse")
def prematch_analyse():

    stats = {
        "avg_goals": 2.4,
        "btts_pct": 42,
        "home_form": 65
    }

    predictions = prematch_engine(stats)

    return {
        "type": "PREMATCH",
        "predictions": predictions
    }
