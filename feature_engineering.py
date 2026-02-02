import pandas as pd

def feature_engineering(df: pd.DataFrame):
    df = df.copy()

    # Drop Time feature (optional)
    if "Time" in df.columns:
        df.drop(columns=["Time"], inplace=True)

    return df
