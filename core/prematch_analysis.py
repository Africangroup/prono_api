def prematch_engine(stats: dict):
    """
    stats: dict contenant avg_goals, btts_pct, home_form, away_form
    Retourne un dictionnaire avec plusieurs paris et score IA global
    """

    predictions = {}

    # Récupération des stats (valeur par défaut = 0 si absent)
    avg_goals = stats.get("avg_goals", 0)
    btts = stats.get("btts_pct", 0)
    home_form = stats.get("home_form", 0)
    away_form = stats.get("away_form", 0)

    # -----------------------------
    # 1️⃣ Over 2.5 Goals
    # -----------------------------
    over_2_5 = {
        "prediction": "Over 2.5 Goals",
        "confidence": 60 + int(avg_goals * 10),  # score IA simple
        "risk": "low" if avg_goals >= 2.5 else "medium"
    }
    predictions["over_2_5_goals"] = over_2_5

    # -----------------------------
    # 2️⃣ BTTS
    # -----------------------------
    btts_pred = {
        "prediction": "BTTS",
        "confidence": 50 + int(btts / 2),
        "risk": "low" if btts >= 50 else "medium"
    }
    predictions["btts"] = btts_pred

    # -----------------------------
    # 3️⃣ Home Win
    # -----------------------------
    home_win = {
        "prediction": "Home Win",
        "confidence": 40 + int(home_form / 2),
        "risk": "low" if home_form >= 60 else "medium"
    }
    predictions["home_win"] = home_win

    # -----------------------------
    # 4️⃣ Away Win
    # -----------------------------
    away_win = {
        "prediction": "Away Win",
        "confidence": 40 + int(away_form / 2),
        "risk": "low" if away_form >= 60 else "medium"
    }
    predictions["away_win"] = away_win

    # -----------------------------
    # 5️⃣ Score IA global (moyenne des confiances)
    # -----------------------------
    total_conf = over_2_5["confidence"] + btts_pred["confidence"] + home_win["confidence"] + away_win["confidence"]
    score_global = int(total_conf / 4)
    predictions["score_global"] = score_global

    return predictions
