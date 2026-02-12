import os
import requests
import websocket
import json
import threading
import time
from datetime import datetime
from supabase_client import supabase  # pour récupérer home/away team IDs
from dotenv import load_dotenv

# ===============================
# 🔹 Chargement des clés
# ===============================
load_dotenv()
API_KEY = os.getenv("bd415d4dffc533b3fba291db92889c1fc9c253b6051711d46c9160d1a6a24229")  # clé API Football
BASE_URL = "https://apiv3.apifootball.com/"

# ===============================
# 🔹 Stockage global des scores live
# ===============================
LIVE_SCORES = {}

# ===============================
# 🔹 Fonctions API Football
# ===============================

def safe_request(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Erreur {func.__name__} :", e)
        return []

def get_lineups(match_id: int):
    url = f"{BASE_URL}?action=get_lineups&match_id={match_id}&APIkey={API_KEY}"
    return requests.get(url, timeout=10).json()

def get_statistics(match_id: int):
    url = f"{BASE_URL}?action=get_statistics&match_id={match_id}&APIkey={API_KEY}"
    return requests.get(url, timeout=10).json()

def get_odds(match_id: int):
    url = f"{BASE_URL}?action=get_odds&match_id={match_id}&APIkey={API_KEY}"
    return requests.get(url, timeout=10).json()

def get_h2h(first_team_id: int, second_team_id: int):
    url = f"{BASE_URL}?action=get_H2H&firstTeamId={first_team_id}&secondTeamId={second_team_id}&APIkey={API_KEY}"
    return requests.get(url, timeout=10).json()

def get_predictions(from_date: str, to_date: str, country_id: int = None, league_id: int = None, match_id: int = None):
    url = f"{BASE_URL}?action=get_predictions&from={from_date}&to={to_date}&APIkey={API_KEY}"
    if country_id: url += f"&country_id={country_id}"
    if league_id: url += f"&league_id={league_id}"
    if match_id: url += f"&match_id={match_id}"
    return requests.get(url, timeout=10).json()

def get_videos(match_id: int = None):
    url = f"{BASE_URL}?action=get_videos&APIkey={API_KEY}"
    if match_id: url += f"&match_id={match_id}"
    return requests.get(url, timeout=10).json()

# ===============================
# 🔹 Fonction complète pour match details
# ===============================
def get_match_details_full(match_id: int, home_team_id: int = None, away_team_id: int = None):
    now = datetime.utcnow().isoformat()

    # Récupération IDs équipes depuis Supabase si non fournis
    if not home_team_id or not away_team_id:
        match = supabase.table("prematch_stats").select("home_team_id, away_team_id").eq("match_id", match_id).execute()
        if match.data:
            home_team_id = match.data[0].get("home_team_id", match_id)
            away_team_id = match.data[0].get("away_team_id", match_id)
        else:
            home_team_id = away_team_id = match_id

    # Données statiques
    lineups = safe_request(get_lineups, match_id)
    stats = safe_request(get_statistics, match_id)
    odds = safe_request(get_odds, match_id)
    videos = safe_request(get_videos, match_id)
    predictions = safe_request(get_predictions, "2023-01-01", "2023-12-31", match_id=match_id)
    h2h = safe_request(get_h2h, home_team_id, away_team_id)

    h2h_summary = {
        "home_last_results": h2h.get("firstTeam_lastResults", []),
        "away_last_results": h2h.get("secondTeam_lastResults", []),
        "head_to_head": h2h.get("firstTeam_vs_secondTeam", [])
    }

    live_data = LIVE_SCORES.get(match_id, {})
    live_stats = {
        "score": f"{live_data.get('match_hometeam_score', 0)} - {live_data.get('match_awayteam_score', 0)}",
        "status": live_data.get("match_status", "N/A"),
        "shots_home": live_data.get("statistiques_1half", [{}])[0].get("domicile", 0) if live_data.get("statistiques_1half") else 0,
        "shots_away": live_data.get("statistiques_1half", [{}])[0].get("loin", 0) if live_data.get("statistiques_1half") else 0,
        "corners_home": live_data.get("statistiques_1half", [{}])[1].get("domicile", 0) if live_data.get("statistiques_1half") and len(live_data["statistiques_1half"]) > 1 else 0,
        "corners_away": live_data.get("statistiques_1half", [{}])[1].get("loin", 0) if live_data.get("statistiques_1half") and len(live_data["statistiques_1half"]) > 1 else 0
    }

    return {
        "match_id": match_id,
        "timestamp": now,
        "lineups": lineups,
        "stats": stats,
        "odds": odds,
        "videos": videos,
        "predictions": predictions,
        "h2h_summary": h2h_summary,
        "live": live_data,
        "live_stats": live_stats
    }

# ===============================
# 🔹 WebSocket scores live
# ===============================
def start_live_scores_ws(api_key: str, timezone: str = "+03:00"):
    url = f"wss://wss.apifootball.com/livescore?APIkey={api_key}&timezone={timezone}"

    def on_message(ws, message):
        data = json.loads(message)
        for match in data:
            match_id = int(match["match_id"])
            LIVE_SCORES[match_id] = match

    def on_error(ws, error):
        print("WebSocket error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed, reconnecting in 5s")
        time.sleep(5)
        threading.Thread(target=start_live_scores_ws, args=(api_key, timezone), daemon=True).start()

    def on_open(ws):
        print("Connected to live scores WebSocket")

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()

def run_live_scores_thread(api_key: str, timezone: str = "+03:00"):
    thread = threading.Thread(target=start_live_scores_ws, args=(api_key, timezone))
    thread.daemon = True
    thread.start()
