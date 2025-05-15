import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

MODEL_PATH = "data/ml_model.joblib"

def train_model_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)

        if "success" not in df.columns:
            print("הקובץ חייב לכלול עמודת 'success' (0 או 1)")
            return

        X = df.drop(columns=["success"])
        y = df["success"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"אחוז דיוק בבדיקה: {round(accuracy * 100, 2)}%")
        print("דו״ח סיווג:\n", classification_report(y_test, y_pred))

        joblib.dump(model, MODEL_PATH)
        print("המודל נשמר אל:", MODEL_PATH)

    except Exception as e:
        print(f"שגיאה באימון המודל: {e}")

def predict_success_probability(features_dict):
    if not os.path.exists(MODEL_PATH):
        print("⚠️ מודל ML לא קיים – חוזר על סף ברירת מחדל")
        return 0.5

    try:
        model = joblib.load(MODEL_PATH)
        df = pd.DataFrame([features_dict])
        probability = model.predict_proba(df)[0][1]
        return round(probability, 3)
    except Exception as e:
        print(f"שגיאה בתחזית ML: {e}")
        return 0.5
