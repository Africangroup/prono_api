from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from ml_models import poisson_prediction, rf_prediction, xgb_prediction, nn_prediction
from api import router as api_router

app = FastAPI(title="PronoAPI Complete", version="6.0")

# --------------------------
# Modèle d'entrée
# --------------------------
class MatchStats(BaseModel):
    team_diff: float
    last10_win_rate: float
    poisson_home_goals: float
    poisson_away_goals: float
    rf_stability_score: float
    momentum: float

# --------------------------
# Health check
# --------------------------
@app.get("/health")
def health_check():
    return {"status": "PronoAPI Complete active 🚀"}

# --------------------------
# Endpoint tout-en-un
# --------------------------
@app.post("/match_stats")
def match_stats(stats: MatchStats):
    df = pd.DataFrame([stats.dict()])

    # --------------------------
    # 1️⃣ Prédictions ML
    # --------------------------
    poisson = poisson_prediction(stats.poisson_home_goals, stats.poisson_away_goals)
    rf = rf_prediction(df)
    xgb_res = xgb_prediction(df)
    nn_res = nn_prediction(df)

    # Combinaison pondérée pour 1X2
    weights = {"xgb": 0.5, "nn": 0.3, "rf": 0.2}
    prob_1 = xgb_res["probabilities"]["1"]*weights["xgb"] + nn_res["probabilities"]["1"]*weights["nn"] + rf["rf_stability_score"]*weights["rf"]
    prob_X = xgb_res["probabilities"]["X"]*weights["xgb"] + nn_res["probabilities"]["X"]*weights["nn"] + (1-rf["rf_stability_score"])*weights["rf"]
    prob_2 = xgb_res["probabilities"]["2"]*weights["xgb"] + nn_res["probabilities"]["2"]*weights["nn"] + (1-rf["rf_stability_score"])*weights["rf"]
    
    final_1X2 = max([("1", prob_1), ("X", prob_X), ("2", prob_2)], key=lambda x:x[1])[0]

    # Double chance simple
    if final_1X2 == "1":
        double_chance = {"1X": 0.9, "12": 0.7, "X2": 0.5}
    elif final_1X2 == "2":
        double_chance = {"1X": 0.5, "12": 0.7, "X2": 0.9}
    else:
        double_chance = {"1X": 0.8, "12": 0.6, "X2": 0.8}

    # --------------------------
    # 2️⃣ Score / Buteurs / Mi-temps (exemple factice)
    # --------------------------
    score = {
        "final_score": "2-1",
        "winner": "Home",
        "goal_scorers": [
            {"player": "John Doe", "team": "Home", "minute": 12},
            {"player": "Jane Smith", "team": "Away", "minute": 35},
            {"player": "John Doe", "team": "Home", "minute": 78}
        ],
        "goals_by_half": {"1H": 2, "2H": 1}
    }

    # --------------------------
    # 3️⃣ Corners
    # --------------------------
    corners = {
        "total": 10,
        "by_team": {"Home": 6, "Away": 4},
        "first_corner": "Home",
        "by_half": {"1H": 5, "2H": 5}
    }

    # --------------------------
    # 4️⃣ Cartons
    # --------------------------
    cards = {
        "total_yellow": 3,
        "total_red": 1,
        "players": [
            {"player": "John Doe", "team": "Home", "card": "yellow", "minute": 23}
        ],
        "by_team": {"Home": {"yellow": 2, "red": 1}, "Away": {"yellow": 1, "red": 0}},
        "by_half": {"1H": {"yellow": 2, "red": 0}, "2H": {"yellow": 1, "red": 1}}
    }

    # --------------------------
    # 5️⃣ Possession
    # --------------------------
    possession = {
        "overall": {"Home": 55, "Away": 45},
        "by_half": {"1H": {"Home": 50, "Away": 50}, "2H": {"Home": 60, "Away": 40}},
        "passes": {"completed": 300, "attempted": 350}
    }

    # --------------------------
    # 6️⃣ Tirs
    # --------------------------
    shots = {
        "total": 15,
        "on_target": 8,
        "by_team": {"Home": {"total": 9, "on_target": 5}, "Away": {"total": 6, "on_target": 3}},
        "by_half": {"1H": 7, "2H": 8}
    }

    # --------------------------
    # 7️⃣ Actions spécifiques
    # --------------------------
    special_actions = {
        "offsides": 2,
        "fouls": {"Home": 8, "Away": 5},
        "saves": {"Home": 4, "Away": 3},
        "penalties": [{"team": "Home", "player": "John Doe", "scored": True}]
    }

    # --------------------------
    # 8️⃣ Stats avancées
    # --------------------------
    advanced_stats = {
        "xG": {"Home": 1.8, "Away": 1.2},
        "xA": {"Home": 1.5, "Away": 0.9},
        "pressing": {"Home": 50, "Away": 45},
        "key_passes": {"Home": 5, "Away": 3}
    }

    # --------------------------
    # 9️⃣ Handicap / Paris spéciaux
    # --------------------------
    special_bets = {
        "asian_handicap": {"Home": -0.25, "Away": +0.25},
        "over_under_goals": 2.5,
        "halftime_fulltime": "1/1",
        "double_chance": {k: round(v*100,2) for k,v in double_chance.items()},
        "over_2_5_prob": round(poisson["over_2_5_prob"]*100,2),
        "btts_prob": round(poisson["btts_prob"]*100,2)
    }

    # --------------------------
    # Résultat final
    # --------------------------
    result = {
        "score": score,
        "corners": corners,
        "cards": cards,
        "possession": possession,
        "shots": shots,
        "special_actions": special_actions,
        "advanced_stats": advanced_stats,
        "special_bets": special_bets
    }

    return result

# --------------------------
# Inclusion autres routes si nécessaire
# --------------------------
app.include_router(api_router)
