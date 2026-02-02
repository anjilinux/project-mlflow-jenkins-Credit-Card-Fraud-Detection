import pandas as pd
from sklearn.preprocessing import RobustScaler

def preprocess_data(df: pd.DataFrame):
    df = df.copy()

    scaler = RobustScaler()
    df["Amount"] = scaler.fit_transform(df[["Amount"]])

    return df
