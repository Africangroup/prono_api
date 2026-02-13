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
    get_videos,
    run_live_scores_thread,
    LIVE_SCORES
)
import os
from dotenv import load_dotenv

# ===============================
# 🔹 Chargement variables .env
# ===============================
load_dotenv()

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")

# ===============================
# 🔹 Initialisation FastAPI
# ===============================
app = FastAPI(title="PRONO API", version="2.0")

# ===============================
# 🔒 Sécurisation API (clé client)
# ===============================
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != CLIENT_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ===============================
# 🚀 Lancement Live Thread
# ===============================
@app.on_event("startup")
def startup_event():
    print("🔴 Démarrage WebSocket Live...")
    if API_FOOTBALL_KEY:
        run_live_scores_thread(API_FOOTBALL_KEY)
    else:
        print("⚠️ API_FOOTBALL_KEY non configurée")

# ===============================
# 🏠 Test API
# ===============================
@app.get("/")
def home():
    return {"status": "PRONO API ACTIVE"}

# ===============================
# 📅 Liste des matchs enregistrés
# ===============================
@app.get("/prematch/list")
def prematch_list(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    response = supabase.table("prematch_stats").select(
        "match_id, home_team, away_team, date"
    ).execute()

    return {"matches": response.data}

# ===============================
# 🧠 Analyse Pré-Match IA
# ===============================
@app.get("/prematch/analyse/{match_id}")
def prematch_analyse(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    response = supabase.table("prematch_stats") \
        .select("*") \
        .eq("match_id", match_id) \
        .execute()

    stats = response.data[0] if response.data else None

    if not stats:
        raise HTTPException(status_code=404, detail="Match stats not found")

    predictions = prematch_engine(stats)

    # Log prédictions
    supabase.table("predictions_log").insert({
        "match_id": match_id,
        "predictions": predictions
    }).execute()

    return {
        "type": "PREMATCH",
        "match_id": match_id,
        "predictions": predictions
    }

# ===============================
# ⚽ Détails complets match
# ===============================
@app.get("/match_details_full/{match_id}")
def match_details_full(
    match_id: int,
    home_team_id: int = None,
    away_team_id: int = None,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    return get_match_details_full(
        match_id,
        home_team_id,
        away_team_id
    )

# ===============================
# 📊 Lineups
# ===============================
@app.get("/lineups/{match_id}")
def lineups(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_lineups(match_id)

# ===============================
# 📊 Statistics
# ===============================
@app.get("/statistics/{match_id}")
def statistics(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_statistics(match_id)

# ===============================
# 💰 Odds
# ===============================
@app.get("/odds/{match_id}")
def odds(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_odds(match_id)

# ===============================
# 🤝 H2H
# ===============================
@app.get("/h2h/{first_team_id}/{second_team_id}")
def h2h(first_team_id: int, second_team_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_h2h(first_team_id, second_team_id)

# ===============================
# 🔮 Predictions API Football
# ===============================
@app.get("/predictions")
def predictions_endpoint(
    from_date: str,
    to_date: str,
    country_id: int = None,
    league_id: int = None,
    match_id: int = None,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)

    return get_predictions(
        from_date,
        to_date,
        country_id,
        league_id,
        match_id
    )

# ===============================
# 🎥 Videos
# ===============================
@app.get("/videos")
def videos(match_id: int = None, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_videos(match_id)

# ===============================
# 🔴 Live Scores
# ===============================
@app.get("/live_scores")
def live_scores_endpoint(
    x_api_key: str = Header(...),
    match_id: int = None,
    league_id: int = None
):
    verify_api_key(x_api_key)

    if not LIVE_SCORES:
        return {"message": "Aucun match live actuellement"}

    results = list(LIVE_SCORES.values())

    if match_id:
        results = [m for m in results if int(m.get("match_id", 0)) == match_id]

    if league_id:
        results = [m for m in results if int(m.get("league_id", 0)) == league_id]

    if not results:
        return {"message": "Aucun résultat correspondant"}

    return {"live_matches": results}
