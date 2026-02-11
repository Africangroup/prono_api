import pandas as pd

memory = pd.read_csv("memory.csv")

def update_rules():
    stats = memory.groupby("bet_type")["result"].value_counts().unstack().fillna(0)

    adjustments = {}

    for bet, row in stats.iterrows():
        wins = row.get("win", 0)
        losses = row.get("loss", 0)

        if losses > wins:
            adjustments[bet] = "risk_up"
        else:
            adjustments[bet] = "risk_down"

    return adjustments
