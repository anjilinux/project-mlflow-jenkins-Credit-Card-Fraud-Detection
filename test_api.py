import requests

def test_api():
    url = "http://localhost:8000/predict"
    payload = {f"V{i}": 0.1 for i in range(1, 29)}
    payload["Amount"] = 0.5

    r = requests.post(url, json=payload)
    assert r.status_code == 200
