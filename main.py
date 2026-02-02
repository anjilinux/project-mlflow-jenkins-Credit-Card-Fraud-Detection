from fastapi import FastAPI
import joblib
import numpy as np

from app.schema import Transaction

app = FastAPI(title="Credit Card Fraud Detection")

model = joblib.load("model.pkl")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(transaction: Transaction):
    data = np.array([list(transaction.dict().values())])
    prediction = model.predict(data)[0]

    return {
        "fraud": int(prediction),
        "label": "Fraud" if prediction == 1 else "Legit"
    }
