# ml_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump, load
import os

MODEL_PATH = "data/ml_model.joblib"

def train_model_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)

        features = df[[
            "rsi", "macd", "volume", "ma_cross",
            "in_demand_zone", "in_buffett_zone",
            "sentiment_score", "weekly_trend", "daily_trend"
        ]]
        target = df["success"]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(features, target)
        dump(model, MODEL_PATH)
        print("מודל ML אומן ונשמר בהצלחה.")

    except Exception as e:
        print(f"שגיאה באימון מודל: {e}")

def predict_success_probability(features_dict):
    try:
        if not os.path.exists(MODEL_PATH):
            print("המודל לא אומן עדיין.")
            return 0.0

        model = load(MODEL_PATH)
        features_df = pd.DataFrame([features_dict])
        prob = model.predict_proba(features_df)[0][1]
        return round(prob, 4)

    except Exception as e:
        print(f"שגיאה בתחזית ML: {e}")
        return 0.0
