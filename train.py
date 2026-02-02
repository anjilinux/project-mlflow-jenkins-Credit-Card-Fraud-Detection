import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import mlflow
import mlflow.sklearn

PROCESSED_DATA_PATH = "clean_data.csv"
MODEL_PATH = "model.pkl"

def train():
    # Load preprocessed data
    df = pd.read_csv(PROCESSED_DATA_PATH)
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # MLflow experiment
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5555"))
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME", "credit-card-fraud"))

    with mlflow.start_run():
        # Train model
        clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
        clf.fit(X_train, y_train)

        # Evaluate
        y_pred = clf.predict(X_test)
        report = classification_report(y_test, y_pred)
        print(report)

        # Log model
        mlflow.sklearn.log_model(clf, "model")
        joblib.dump(clf, MODEL_PATH)
        print(f"✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()
