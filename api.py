from fastapi import FastAPI, Header, HTTPException
from core.prematch_analysis import prematch_engine
from supabase_client import supabase
from apifootball_client import (
    get_match_details_full,
    get_lineups,
    get_statistics,
    get_odds,
    get_h2h,
    get_predictions,
    get_videos
)
import threading
import websocket
import json
import time
from apifootball_client import run_live_scores_thread, API_KEY

# Lancer le suivi live dès le démarrage
run_live_scores_thread(API_KEY)

app = FastAPI(title="PRONO API", version="1.0")

# ===============================
# 🔒 Clé API pour sécuriser les endpoints
# ===============================
API_KEY = "bd415d4dffc533b3fba291db92889c1fc9c253b6051711d46c9160d1a6a24229"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ===============================
# 🔵 Endpoint Test
# ===============================
@app.get("/")
def home():
    return {"status": "API PRONO ACTIVE"}

# ===============================
# 🔵 Liste des matchs disponibles
# ===============================
@app.get("/prematch/list")
def prematch_list(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    response = supabase.table("prematch_stats").select("match_id, home_team, away_team, date").execute()
    return {"matches": response.data}

# ===============================
# 🔴 Analyse pré-match dynamique
# ===============================
@app.get("/prematch/analyse/{match_id}")
def prematch_analyse(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    response = supabase.table("prematch_stats").select("*").eq("match_id", match_id).execute()
    stats = response.data[0] if response.data else None

    if not stats:
        return {"error": "Match stats not found"}

    predictions = prematch_engine(stats)

    supabase.table("predictions_log").insert({
        "match_id": match_id,
        "predictions": predictions,
    }).execute()

    return {
        "type": "PREMATCH",
        "match_id": match_id,
        "predictions": predictions
    }

# ===============================
# 🔵 Match Details Full (lineups + stats + odds + h2h + videos + predictions)
# ===============================
@app.get("/match_details_full_live/{match_id}")
async def match_details_full_live(
    match_id: int, 
    home_team_id: int = None, 
    away_team_id: int = None, 
    x_api_key: str = Header(...)
):
    """
    Endpoint LIVE ULTRA COMPLÈT :
    - Lineups, stats, odds, videos, predictions
    - H2H enrichi
    - Stats live cumulées + historique live
    """
    verify_api_key(x_api_key)
    data = get_match_details_full_v5(match_id, home_team_id, away_team_id)
    return data

# ===============================
# 🔵 Lineups
# ===============================
@app.get("/lineups/{match_id}")
async def lineups(match_id: int):
    return get_lineups(match_id)

# ===============================
# 🔵 Statistics
# ===============================
@app.get("/statistics/{match_id}")
async def statistics(match_id: int):
    return get_statistics(match_id)

# ===============================
# 🔵 Odds
# ===============================
@app.get("/odds/{match_id}")
async def odds(match_id: int):
    return get_odds(match_id)

# ===============================
# 🔵 H2H
# ===============================
@app.get("/h2h/{first_team_id}/{second_team_id}")
async def h2h(first_team_id: int, second_team_id: int):
    return get_h2h(first_team_id, second_team_id)

# ===============================
# 🔵 Predictions
# ===============================
@app.get("/predictions")
async def predictions_endpoint(
    from_date: str,
    to_date: str,
    country_id: int = None,
    league_id: int = None,
    match_id: int = None
):
    return get_predictions(from_date, to_date, country_id, league_id, match_id)

# ===============================
# 🔵 Videos
# ===============================
@app.get("/videos")
async def videos(match_id: int = None):
    return get_videos(match_id)

# ===============================
# 🔵 Live Scores via WebSocket (optimisé avec filtres)
# ===============================
LIVE_SCORES = {}

def start_live_scores_ws(api_key: str, timezone: str = "+03:00"):
    url = f"wss://wss.apifootball.com/livescore?APIkey={api_key}&timezone={timezone}"

    def on_message(ws, message):
        global LIVE_SCORES
        try:
            data = json.loads(message)
            for match in data:
                match_id = match.get("match_id")
                if match_id:
                    LIVE_SCORES[match_id] = match
        except Exception as e:
            print("Erreur parsing WS message:", e)

    def on_error(ws, error):
        print("WebSocket error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed, reconnecting...")
        time.sleep(5)
        start_live_scores_ws(api_key, timezone)

    def on_open(ws):
        print("Connecté au WebSocket live scores")

    ws = websocket.WebSocketApp(
        url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    ws.run_forever()

# Lancer le WebSocket dans un thread séparé
threading.Thread(target=start_live_scores_ws, args=(API_KEY,), daemon=True).start()

# Endpoint filtrable par match_id et league_id
@app.get("/live_scores")
async def live_scores_endpoint(
    x_api_key: str = Header(...),
    match_id: int = None,
    league_id: int = None
):
    verify_api_key(x_api_key)

    if not LIVE_SCORES:
        return {"message": "Aucun score en direct pour le moment"}

    results = list(LIVE_SCORES.values())

    # Filtrer par match_id
    if match_id:
        results = [m for m in results if int(m.get("match_id", 0)) == match_id]

    # Filtrer par league_id
    if league_id:
        results = [m for m in results if int(m.get("league_id", 0)) == league_id]

    if not results:
        return {"message": "Aucun score correspondant aux filtres"}

    return {"live_scores": results}
