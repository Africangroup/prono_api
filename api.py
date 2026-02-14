# api.py

from fastapi import APIRouter, Header, HTTPException
from supabase_client import supabase
from core.prematch_analysis import prematch_engine
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
import requests
from datetime import datetime
from dotenv import load_dotenv

# ===============================
# 🔹 Chargement variables d'environnement
# ===============================
load_dotenv()

API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY")

router = APIRouter()

# ===============================
# 🔒 Vérification clé API
# ===============================
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != CLIENT_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ===============================
# 🚀 Lancement Thread Live Scores
# ===============================
@router.on_event("startup")
def startup_event():
    print("🔴 Démarrage WebSocket Live...")
    if API_FOOTBALL_KEY:
        run_live_scores_thread(API_FOOTBALL_KEY)
    else:
        print("⚠️ API_FOOTBALL_KEY non configurée")

# ===============================
# 📅 Liste des matchs Supabase
# ===============================
@router.get("/prematch/list")
def prematch_list(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    response = supabase.table("prematch_stats").select(
        "match_id, home_team, away_team, date"
    ).execute()

    return {"matches": response.data}

# ===============================
# ⚡ Sync Matches (format VrSOCCER)
# ===============================
@router.get("/sync-matches")
def sync_matches(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    today = datetime.now().strftime("%Y-%m-%d")
    url = "https://apiv3.apifootball.com"

    params = {
        "action": "get_events",
        "from": today,
        "to": today,
        "APIkey": API_FOOTBALL_KEY
    }

    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail="API-Football error"
        )

    data = resp.json()

    matches = []
    for match in data:
        try:
            matches.append({
                "match_id": int(match["match_id"]),
                "league_id": int(match["league_id"]),
                "home_team_id": int(match["match_hometeam_id"]),
                "away_team_id": int(match["match_awayteam_id"]),
                "home_team": match["match_hometeam_name"],
                "away_team": match["match_awayteam_name"],
                "date": match["match_date"] + "T" + match["match_time"] + "Z"
            })
        except (KeyError, ValueError):
            continue

    return {"matches": matches, "date": today}

# ===============================
# 📅 Matchs du jour API-Football
# ===============================
@router.get("/matches/today")
def matches_today(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    today = datetime.now().strftime("%Y-%m-%d")
    url = "https://apiv3.apifootball.com"

    params = {
        "action": "get_events",
        "from": today,
        "to": today,
        "APIkey": API_FOOTBALL_KEY
    }

    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail="API-Football error"
        )

    return resp.json()

# ===============================
# 📊 Lineups
# ===============================
@router.get("/lineups/{match_id}")
def lineups(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_lineups(match_id)

# ===============================
# 📊 Statistics
# ===============================
@router.get("/statistics/{match_id}")
def statistics(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_statistics(match_id)

# ===============================
# 💰 Odds
# ===============================
@router.get("/odds/{match_id}")
def odds(match_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_odds(match_id)

# ===============================
# 🔁 H2H
# ===============================
@router.get("/h2h/{first_team_id}/{second_team_id}")
def h2h(first_team_id: int, second_team_id: int, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_h2h(first_team_id, second_team_id)

# ===============================
# 🤖 Predictions
# ===============================
@router.get("/predictions")
def predictions_endpoint(
    from_date: str,
    to_date: str,
    country_id: int = None,
    league_id: int = None,
    match_id: int = None,
    x_api_key: str = Header(...)
):
    verify_api_key(x_api_key)
    return get_predictions(from_date, to_date, country_id, league_id, match_id)

# ===============================
# 🎥 Videos
# ===============================
@router.get("/videos")
def videos(match_id: int = None, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return get_videos(match_id)

# ===============================
# 🔴 Live Scores
# ===============================
@router.get("/live_scores")
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
