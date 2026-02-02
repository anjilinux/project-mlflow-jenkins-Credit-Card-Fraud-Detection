# schema.py
from pydantic import BaseModel, Field
import pandas as pd
import sys
import os

# ----------------------------
# Model Input Schema
# ----------------------------
class FraudInputSchema(BaseModel):
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float = Field(..., gt=0)

# ----------------------------
# Dataset Schema Validation
# ----------------------------
EXPECTED_COLUMNS = [
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28","Amount","Class"
]

def validate_dataset_schema(csv_path: str):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)

    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS)

    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if extra:
        raise ValueError(f"Unexpected columns: {extra}")

    print("✅ Dataset schema validation passed")

# ----------------------------
# Jenkins Entry Point
# ----------------------------
if __name__ == "__main__":
    try:
        validate_dataset_schema("data/processed/processed_data.csv")
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        sys.exit(1)
