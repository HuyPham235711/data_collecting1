import requests
import os
from dotenv import load_dotenv
import pandas as pd


def get_api_key(apikey_path):
    load_dotenv(apikey_path)
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API key not found.")
    print("API key loaded successfully.")
    return api_key

def construct_url(apikey, function, symbol, interval):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        "apikey": apikey
    }
    return url, params

def fetch_intraday_data(apikey, function, interval, symbol="TSLA"):
    url, params = construct_url(apikey, function, symbol, interval)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            print("Data fetched successfully.")
            return data
        else:
            raise ValueError("Unexpected data format or empty response.")
    except requests.exceptions.RequestException as e:
        print("API request error:", e)
        return None

def save_raw_data(data, filename="TSLA1.json"):
    if data:
        filepath = os.path.join(".", "data", "raw", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            pd.DataFrame(data).to_json(f, orient="records", indent=4)
        print("Data saved successfully.")
    else:
        print("No data to save.")