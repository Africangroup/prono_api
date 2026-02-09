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

import pandas as pd
import requests
from datetime import datetime

BOT_TOKEN = "8280231709:AAG_McGLnUJ0WQp0K5zMtNqMQP8Ia9smWRs"
CHAT_ID = "8280231709"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

@app.get("/alert")
def alert():
    df = pd.read_csv("data/live_training.csv")

    if df.empty:
        return {"status": "no data"}

    row = df.iloc[-1]

    minute = int(row["minute"])
    shots = int(row["shots_total"])
    xg = float(row["xg_total"])
    fouls = int(row["fouls_total"])
    proba = float(row["proba_goal"])

    if (
        minute >= 60 and
        proba >= 0.65 and
        shots >= 12 and
        xg >= 1.5 and
        fouls <= 22
    ):
        stake = round(min(10, (proba - 0.5) * 50), 2)

        message = (
            f"🔥 BET AUTORISÉ\n\n"
            f"⏱ Minute : {minute}\n"
            f"📊 Proba : {proba}\n"
            f"📈 xG : {xg}\n"
            f"🎯 Tirs : {shots}\n"
            f"🚫 Fautes : {fouls}\n"
            f"💰 Mise conseillée : {stake} €\n"
            f"🕒 {datetime.now().strftime('%H:%M:%S')}"
        )

        send_telegram(message)

        return {
            "bet": True,
            "message": "Alert sent",
            "stake": stake
        }

    return {"bet": False}

