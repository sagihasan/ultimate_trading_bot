import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

MODEL_PATH = "data/model.pkl"
DATA_PATH = "data/training_data.csv"

def train_model():
    data = pd.read_csv(DATA_PATH)
    X = data.drop(columns=["success"])
    y = data["success"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
