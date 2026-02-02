import pandas as pd
import joblib
from sklearn.metrics import classification_report

def evaluate():
    df = pd.read_csv("clean_data.csv")
    model = joblib.load("model.pkl")

    X = df.drop("Class", axis=1)
    y = df["Class"]

    preds = model.predict(X)
    print(classification_report(y, preds))

if __name__ == "__main__":
    evaluate()
