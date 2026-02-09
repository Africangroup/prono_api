import pandas as pd
import requests
from datetime import datetime

memory = pd.read_csv("memory.csv")

if len(memory) >= 20:
    taux_reussite = memory["result"].mean()
    MIN_PROBA = 0.65 if taux_reussite < 0.55 else 0.60
else:
    MIN_PROBA = 0.60



BOT_TOKEN = "8280231709:AAG_McGLnUJ0WQp0K5zMtNqMQP8Ia9smWRs"
CHAT_ID = "8280231709"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

df = pd.read_csv("data/live_training.csv")

if df.empty:
    exit()

row = df.iloc[-1]

minute = int(row["minute"])
shots = int(row["shots_total"])
xg = float(row["xg_total"])
fouls = int(row["fouls_total"])
proba = float(row["proba_goal"])

if (
    minute >= 60 and
    proba >= MIN_PROBA and
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

    print(message)
    send_telegram(message)

else:
    print("⛔ PAS DE PARI")




