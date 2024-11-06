import pandas as pd
import json
import os

def load_json(filepath):
    try:
        with open(filepath) as f:
            data = json.load(f)
        print(f"Data loaded from {filepath}.")
        return data
    except FileNotFoundError:
        print(f"File not found: {filepath}.")
        return None

def extract_trading_data(data):
    if not data:
        print ("No data provided fo extraction.")
        return None
    
    trading_data = [
                    entry["Time Series (5min)"] 
                    for entry in data 
                    if entry["Time Series (5min)"] is not None]

    df = pd.DataFrame(trading_data)
    df.columns = ["open", "high", "low", "close", "volume"]
    df.apply(pd.to_numeric, errors='coerce')
    print("Data extracted successfully.")
    return df

def clean_data(filepath):
    raw_data = load_json(filepath)
    cleaned_data = extract_trading_data(raw_data)
    return cleaned_data

def save_to_csv(df, output_filepath):
    if df is not None:
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        df.to_csv(output_filepath, index=False)
        print(f"Data saved to {output_filepath}.")
    else:
        print("No DataFrame provided to save.")

def process_json_to_csv(input_filepath, output_filepath):
    raw_data = load_json(input_filepath)
    clean_data = extract_trading_data(raw_data)
    save_to_csv(clean_data, output_filepath)

