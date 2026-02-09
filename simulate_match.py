import time
import pandas as pd
import random
import subprocess

print("⚽ Simulation du match en cours...\n")

goals = 0
shots = 0
xg = 0.0
fouls = 0

for minute in range(1, 91):

    shots += random.randint(0, 2)
    fouls += random.randint(0, 1)
    xg += round(random.uniform(0.01, 0.06), 2)

    if random.random() < 0.05:
        goals += 1

    proba_goal = round(min(0.9, xg / (goals + 1)), 2)

    df = pd.DataFrame([{
        "minute": minute,
        "goals_total": goals,
        "shots_total": shots,
        "xg_total": xg,
        "fouls_total": fouls,
        "proba_goal": proba_goal
    }])

    df.to_csv("data/live_training.csv", index=False)

    print(f"⏱️ Minute {minute} | Proba: {proba_goal}")

    subprocess.run(["C:\\Python313\\python.exe", "bet_decision.py"])

    time.sleep(1)
