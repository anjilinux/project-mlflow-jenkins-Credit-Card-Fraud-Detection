import pandas as pd

def test_data_load():
    df = pd.read_csv("clean_data.csv")
    assert not df.empty
    assert "Class" in df.columns
