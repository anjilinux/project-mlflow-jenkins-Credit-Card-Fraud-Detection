import pandas as pd
import os
from sklearn.preprocessing import StandardScaler

# Paths
RAW_DATA_PATH = "creditcard.csv"
PROCESSED_DATA_PATH = "clean_data.csv"

def preprocess_data():
    # Make processed directory if not exists
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)

    # Load raw data
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"📊 Raw data shape: {df.shape}")

    # Check for missing values
    if df.isnull().sum().sum() > 0:
        print("⚠️ Missing values found, filling with 0")
        df.fillna(0, inplace=True)

    # Scale Amount column
    scaler = StandardScaler()
    df["Amount"] = scaler.fit_transform(df[["Amount"]])

    # Ensure all columns are numeric
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    df = df[numeric_cols]

    # Save cleaned data
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"✅ Clean data saved: {PROCESSED_DATA_PATH}")
    print(f"📊 Clean data shape: {df.shape}")

if __name__ == "__main__":
    preprocess_data()
