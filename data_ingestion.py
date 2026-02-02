import pandas as pd
import os

RAW_DATA_PATH = "creditcard.csv"
PROCESSED_DATA_PATH = "clean_data.csv"

def load_raw_data():
    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError("Raw data not found")
    return pd.read_csv(RAW_DATA_PATH)

def save_processed_data(df):
    os.makedirs("processed", exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

if __name__ == "__main__":
    df = load_raw_data()
    save_processed_data(df)
