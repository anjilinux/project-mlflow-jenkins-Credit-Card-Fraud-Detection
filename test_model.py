import joblib
import numpy as np

def test_model_prediction():
    model = joblib.load("model.pkl")
    sample = np.random.rand(1, 29)
    pred = model.predict(sample)
    assert pred[0] in [0, 1]
