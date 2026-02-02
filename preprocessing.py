import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Use Jenkins workspace-relative paths
RAW_DATA_PATH = os.path.join(os.getcwd(), "creditcard.csv")
PROCESSED_DATA_PATH = os.path.join(os.getcwd(), "clean_data.csv")

def preprocess_data():
    # Ensure the processed directory exists
    processed_dir = os.path.dirname(PROCESSED_DATA_PATH)
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir, exist_ok=True)

    # Load raw data
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data file not found: {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"📊 Raw data shape: {df.shape}")

    # Fill missing values
    if df.isnull().sum().sum() > 0:
        df.fillna(0, inplace=True)

    # Scale Amount
    scaler = StandardScaler()
    df["Amount"] = scaler.fit_transform(df[["Amount"]])

    # Keep numeric columns only
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df = df[numeric_cols]

    # Save processed data
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"✅ Clean data saved at {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess_data()
