from fastapi import FastAPI
from pydantic import BaseModel
from api import router as api_router
from ml_models import poisson_prediction, rf_prediction, xgb_prediction, nn_prediction
import pandas as pd

app = FastAPI(title="PronoAPI Ultimate", version="4.0")

class MatchStats(BaseModel):
    team_diff: float
    last10_win_rate: float
    poisson_home_goals: float
    poisson_away_goals: float
    rf_stability_score: float
    momentum: float

@app.get("/health")
def health_check():
    return {"status": "PronoAPI Ultimate active 🚀"}

@app.post("/predict")
def predict_all(stats: MatchStats):
    df = pd.DataFrame([stats.dict()])

    poisson = poisson_prediction(stats.poisson_home_goals, stats.poisson_away_goals)
    rf = rf_prediction(df)
    xgb_res = xgb_prediction(df)
    nn = nn_prediction(df)

    # Double chance simple basé sur XGBoost
    xgb_label = xgb_res['prediction_1X2']
    if xgb_label == '1':
        double_chance = {"1X": 90, "12": 70, "X2": 50}
    elif xgb_label == '2':
        double_chance = {"1X": 50, "12": 70, "X2": 90}
    else:
        double_chance = {"1X": 80, "12": 60, "X2": 80}

    result = {
        "poisson": poisson,
        "rf": rf,
        "xgb": xgb_res,
        "nn": nn,
        "double_chance": double_chance
    }
    return result

# Inclure les autres routes si besoin
app.include_router(api_router)
