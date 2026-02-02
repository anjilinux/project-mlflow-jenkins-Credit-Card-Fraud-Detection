import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

RAW_DATA_PATH = "creditcard.csv"
PROCESSED_DATA_PATH = "clean_data.csv"

def preprocess_data():
    # Make sure the processed directory exists
    processed_dir = os.path.dirname(PROCESSED_DATA_PATH)
    if processed_dir == "":
        processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    # Load raw data
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"📊 Raw data shape: {df.shape}")

    # Fill missing values if any
    if df.isnull().sum().sum() > 0:
        df.fillna(0, inplace=True)

    # Scale Amount
    scaler = StandardScaler()
    df["Amount"] = scaler.fit_transform(df[["Amount"]])

    # Keep only numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df = df[numeric_cols]

    # Save processed data
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"✅ Clean data saved at {PROCESSED_DATA_PATH}")

# Correct indentation here
if __name__ == "__main__":
    preprocess_data()
