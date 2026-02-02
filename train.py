import mlflow
import mlflow.sklearn
import pandas as pd
import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, precision_score, roc_auc_score

from preprocessing import preprocess_data
from feature_engineering import feature_engineering
from utils import split_data

DATA_PATH = "clean_data.csv"

mlflow.set_tracking_uri("http://localhost:5555")
mlflow.set_experiment("Credit_Card_Fraud_Detection")

def train():
    df = pd.read_csv(DATA_PATH)

    df = preprocess_data(df)
    df = feature_engineering(df)

    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = split_data(X, y)

    model = LogisticRegression(class_weight="balanced", max_iter=1000)

    with mlflow.start_run():
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mlflow.log_metric("precision", precision_score(y_test, y_pred))
        mlflow.log_metric("recall", recall_score(y_test, y_pred))
        mlflow.log_metric("f1_score", f1_score(y_test, y_pred))
        mlflow.log_metric("roc_auc", roc_auc_score(y_test, y_pred))

        mlflow.sklearn.log_model(model, "model")

        joblib.dump(model, "model.pkl")
        mlflow.log_artifact("model.pkl")

if __name__ == "__main__":
    train()
