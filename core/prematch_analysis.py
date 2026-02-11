def prematch_engine(stats: dict):

    avg_goals = stats.get("avg_goals", 0)
    btts = stats.get("btts_pct", 0)
    home_form = stats.get("home_form", 0)

    prediction = "NO BET"
    confidence = 50

    if avg_goals >= 2.5 and home_form >= 60:
        prediction = "Over 2.5 Goals"
        confidence = 72

    elif btts >= 50:
        prediction = "BTTS"
        confidence = 68

    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk": "low" if confidence >= 70 else "medium"
    }
