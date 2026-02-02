import os
import pandas as pd

def test_clean_data_exists():
    assert os.path.exists("clean_data.csv"), "Clean data CSV not found!"

def test_data_not_empty():
    df = pd.read_csv("clean_data.csv")
    assert not df.empty, "Clean data CSV is empty!"
