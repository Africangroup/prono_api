import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# ===============================
# Poisson
# ===============================
def poisson_prediction(home_goals, away_goals):
    total_goals = home_goals + away_goals
    over_2_5_prob = round(np.clip(total_goals / 5, 0, 1) * 100, 2)
    btts_prob = round(np.clip((home_goals > 0) & (away_goals > 0), 0, 1) * 100, 2)
    return {"home_expected_goals": home_goals,
            "away_expected_goals": away_goals,
            "over_2_5_prob": over_2_5_prob,
            "btts_prob": btts_prob}

# ===============================
# Random Forest
# ===============================
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5)
def rf_prediction(df):
    return {"rf_stability_score": 0.85}

# ===============================
# XGBoost
# ===============================
data_xgb = pd.DataFrame({
    'team_diff': [1, -1, 0, 2],
    'last10_win_rate': [0.6, 0.3, 0.5, 0.8],
    'poisson_home_goals': [2, 1, 1, 3],
    'poisson_away_goals': [1, 2, 0, 1],
    'rf_stability_score': [0.9, 0.6, 0.8, 0.95],
    'momentum': [1, -1, 0, 2],
    'result_1X2': ['1', '2', 'X', '1']
})
xgb_label_encoder = LabelEncoder()
data_xgb['result_encoded'] = xgb_label_encoder.fit_transform(data_xgb['result_1X2'])
features_xgb = ['team_diff','last10_win_rate','poisson_home_goals',
                'poisson_away_goals','rf_stability_score','momentum']
xgb_model = xgb.XGBClassifier(
    n_estimators=200, max_depth=4, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.9,
    use_label_encoder=False, eval_metric='mlogloss'
)
xgb_model.fit(data_xgb[features_xgb], data_xgb['result_encoded'])

def xgb_prediction(df):
    pred_encoded = xgb_model.predict(df)
    pred_label = xgb_label_encoder.inverse_transform(pred_encoded)[0]
    proba = xgb_model.predict_proba(df)[0]
    prob_dict = {label: round(float(proba[i])*100,2) 
                 for i,label in enumerate(xgb_label_encoder.classes_)}
    return {"prediction_1X2": pred_label,"probabilities_percent": prob_dict}

# ===============================
# Neural Network
# ===============================
nn_model = Sequential([
    Dense(32, activation="relu", input_shape=(6,)),
    Dense(16, activation="relu"),
    Dense(3, activation="softmax")
])
def nn_prediction(df):
    return {"nn_probabilities": [0.6, 0.2, 0.2]}
