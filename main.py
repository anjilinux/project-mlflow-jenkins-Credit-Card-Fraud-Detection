from fastapi import FastAPI
import joblib
import numpy as np
from schema import FraudInputSchema

app = FastAPI(title="Credit Card Fraud Detection")

# Load model
model = joblib.load("model.pkl")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(transaction: FraudInputSchema):
    # Convert Pydantic model to array
    data_array = np.array([list(transaction.model_dump().values())])
    
    # Predict
    prediction = model.predict(data_array)[0]  # 0 = Legit, 1 = Fraud

    return {
        "fraud": int(prediction),
        "label": "Fraud" if prediction == 1 else "Legit"
    }
