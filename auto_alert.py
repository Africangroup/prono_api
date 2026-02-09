import time
import requests

API_URL = "http://127.0.0.1:8000/signal"

print("🤖 Bot d’alerte lancé...")

last_alert = False

while True:
    try:
        r = requests.get(API_URL, timeout=5)
        data = r.json()

        bet = data["bet"]
        minute = data["minute"]
        proba = data["proba_goal"]

        if bet and not last_alert:
            print("\n🚨🚨🚨 ALERTE BET 🚨🚨🚨")
            print(f"⏱️ Minute : {minute}")
            print(f"⚽ Proba but : {proba}")
            print("🔥 OPPORTUNITÉ DÉTECTÉE 🔥\n")

            last_alert = True

        if not bet:
            last_alert = False

    except Exception as e:
        print("⚠️ Erreur API :", e)

    time.sleep(30)  # vérifie toutes les 30 secondes
