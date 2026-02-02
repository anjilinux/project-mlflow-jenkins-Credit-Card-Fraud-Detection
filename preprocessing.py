import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

RAW_DATA_PATH = os.path.join(os.getcwd(), "creditcard.csv")
PROCESSED_DATA_PATH = os.path.join(os.getcwd(), "clean_data.csv")

def preprocess_data():
    # Ensure directory exists
    processed_dir = os.path.dirname(PROCESSED_DATA_PATH)
    os.makedirs(processed_dir, exist_ok=True)

    df = pd.read_csv(RAW_DATA_PATH)
    df.fillna(0, inplace=True)

    scaler = StandardScaler()
    df["Amount"] = scaler.fit_transform(df[["Amount"]])

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df = df[numeric_cols]

    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"✅ Clean data saved at {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    preprocess_data()
