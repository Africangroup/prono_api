from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class MatchData(BaseModel):
    home_form: float
    away_form: float
    home_goals: float
    away_goals: float
    home: int

@app.get("/")
def home():
    return {"message": "API Pronostics active"}

@app.post("/predict")
def predict(data: MatchData):
    home_win = round(random.uniform(45, 70), 2)
    draw = round(random.uniform(10, 25), 2)
    away_win = round(100 - home_win - draw, 2)

    return {
        "home_win": home_win,
        "draw": draw,
        "away_win": away_win,
        "recommendation": "Victoire domicile" if home_win > away_win else "Victoire extérieur"
    }
