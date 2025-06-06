from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

def calculate_ai_score(features_dict):
    try:
        model = joblib.load(MODEL_PATH)
        df = pd.DataFrame([features_dict])
        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1]
        return {
            "ai_score": float(proba),
            "confidence": round(proba, 2),
            "prediction": int(prediction)
        }
    except Exception as e:
        return {
            "ai_score": 0.0,
            "confidence": 0.0,
            "prediction": 0,
            "error": str(e)
        }

# הגדרות נתיב
MODEL_PATH = "data/model.pkl"
DATA_PATH = "data/training_data.csv"

# אימון המודל ML
def train_model():
    try:
        print("התחלתי לאמן את המודל...")
        data = pd.read_csv(DATA_PATH)
        X = data.drop(columns=["success"])
        y = data["success"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)

        accuracy = accuracy_score(y_test, model.predict(X_test))
        print(f"אחוז דיוק: {round(accuracy * 100, 2)}%")

        joblib.dump(model, MODEL_PATH)
        print(f"המודל נשמר ב־{MODEL_PATH}")

    except Exception as e:
        print(f"שגיאה באימון המודל: {e}")

if __name__ == "__main__":
    train_model()
