# ml_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = "data/model.pkl"
DATA_PATH = "data/training_data.csv"

# אימון מודל ML
def train_model():
    try:
        data = pd.read_csv(DATA_PATH)

        X = data.drop(columns=["result"])
        y = data["result"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        accuracy = accuracy_score(y_test, model.predict(X_test))
        print(f"דיוק המודל: {round(accuracy * 100, 2)}%")

        joblib.dump(model, MODEL_PATH)
        print("המודל נשמר בהצלחה.")
        return model

    except Exception as e:
        print(f"שגיאה באימון המודל: {e}")
        return None

# טוען או מאמן מודל חדש
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_model()

# חישוב ניקוד AI למניה מסוימת
def calculate_ai_score(features_dict):
    try:
        model = load_model()
        if model is None:
            return 0

        df = pd.DataFrame([features_dict])
        prob = model.predict_proba(df)[0][1]  # הסתברות להצלחה
        ai_score = int(prob * 100)
        return ai_score

    except Exception as e:
        print(f"שגיאה בחישוב AI Score: {e}")
        return 0
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

MODEL_PATH = "data/model.pkl"
DATA_PATH = "data/training_data.csv"

# אימון מודל ML
def train_model():
    try:
        data = pd.read_csv(DATA_PATH)

        X = data.drop(columns=["result"])
        y = data["result"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        accuracy = accuracy_score(y_test, model.predict(X_test))
        print(f"דיוק המודל: {round(accuracy * 100, 2)}%")

        joblib.dump(model, MODEL_PATH)
        print("המודל נשמר בהצלחה.")
        return model

    except Exception as e:
        print(f"שגיאה באימון המודל: {e}")
        return None

# טוען או מאמן מודל חדש
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_model()

# חישוב ניקוד AI למניה מסוימת
def calculate_ai_score(features_dict):
    try:
        model = load_model()
        if model is None:
            return 0

        df = pd.DataFrame([features_dict])
        prob = model.predict_proba(df)[0][1]  # הסתברות להצלחה
        ai_score = int(prob * 100)
        return ai_score

    except Exception as e:
        print(f"שגיאה בחישוב AI Score: {e}")
        return 0
