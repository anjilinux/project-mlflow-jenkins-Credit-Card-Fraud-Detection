from fastapi import FastAPI
import joblib
import numpy as np
from schema import FraudInputSchema

app = FastAPI(title="Credit Card Fraud Detection")

# Load trained model
model = joblib.load("model.pkl")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: FraudInputSchema):
    # Convert Pydantic model → numpy array
    features = np.array([list(data.model_dump().values())])

    # Predict
    prediction = int(model.predict(features)[0])

    return {
        "fraud": prediction,
        "label": "Fraud" if prediction == 1 else "Legit"
    }
