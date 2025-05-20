from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

# הגדרות נתיב
MODEL_PATH = "data/model.pkl"
DATA_PATH = "data/training_data.csv"

# אימון המודל ML
def train_model():
    try:
        # קריאת הנתונים
        data = pd.read_csv(DATA_PATH)

        # הפרדת מאפיינים ותגית
        X = data.drop(columns=["success"])
        y = data["success"]

        # פיצול ל־Train ו־Test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # יצירת המודל ואימון
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # חישוב דיוק
        accuracy = accuracy_score(y_test, model.predict(X_test))
        print(f"אחוז דיוק: {round(accuracy * 100, 2)}%")

        # שמירת המודל
        joblib.dump(model, MODEL_PATH)

    except Exception as e:
        print(f"שגיאה באימון המודל: {e}")
