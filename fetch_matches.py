import os
import requests
import pandas as pd
from dotenv import load_dotenv
import time

# Charger la clé depuis .env
load_dotenv()
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_FOOTBALL_KEY:
    raise ValueError("Clé API-Football manquante dans .env")

# Paramètres
league_id = 39       # Premier League
season = 2025        # Saison 2025-26

# URL de l'API
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

headers = {
    "X-RapidAPI-Key": API_FOOTBALL_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

params = {"league": league_id, "season": season}

# Requête API
response = requests.get(url, headers=headers, params=params)

# Vérification réponse
if response.status_code == 200:
    data = response.json().get('response', [])
    if not data:
        print("Aucun match récupéré !")
    else:
        matches = []
        for match in data:
            matches.append({
                "match_id": match["fixture"]["id"],
                "date": match["fixture"]["date"],
                "home_team": match["teams"]["home"]["name"],
                "away_team": match["teams"]["away"]["name"],
                "home_goals": match["goals"]["home"],
                "away_goals": match["goals"]["away"]
            })
        # Convertir en DataFrame et sauvegarder
        df = pd.DataFrame(matches)
        df.to_csv("premier_league_2025_26.csv", index=False)
        print(f"✅ {len(df)} matchs récupérés !")
        print(df.head())
elif response.status_code == 401:
    print("❌ Clé API invalide ou inactive (401)")
elif response.status_code == 403:
    print("❌ Vous n’êtes pas abonné à l’API (403)")
elif response.status_code == 429:
    print("❌ Trop de requêtes ! Limite API atteinte (429)")
else:
    print(f"❌ Erreur {response.status_code} : {response.text}")

# Petite pause pour éviter 429 si plusieurs requêtes
time.sleep(1)
