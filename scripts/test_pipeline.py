import os
import unittest
import pandas as pd
from api_integration import get_api_key, fetch_intraday_data
from data_cleansing import clean_data
from data_storage import connect_to_db, store_data

class TestPipline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.api_key_path = os.path.join("..", "apikey.env")
        cls.processed_data_path = os.path.join("..", "data", "processed", "TSLA1.csv")
        cls.raw_data_path = os.path.join("..", "data", "raw", "TSLA1.json")
        cls.symbol = "TSLA"
        cls.interval = "5min"
        cls.server = 'CAUBEKINH8\SQLEXPRESS' # Update with your server name
        cls.database = 'traday_TSLA'
        cls.table_name = "intraday_data_tsla"

    def test_fetch_data(self):
        data = fetch_intraday_data(get_api_key(self.api_key_path),"TIME_SERIES_INTRADAY",  self.interval, self.symbol)
        self.assertIsNotNone(data, "No data fetched from API.")
        self.assertIn("Time Series (5min)", data, "Time series data not found in response.")
    
    def test_clean_data(self):
        df = clean_data(self.raw_data_path)
        self.assertIsNotNone(df, "Data is not a DataFrame.")
        self.assertFalse(df.empty, "DataFrame is empty.")
    
    def test_store_data(self):
        store_data(self.processed_data_path, self.server, self.database, self.table_name)
        
        conn = connect_to_db(self.server, self.database)
        query = f"SELECT COUNT(*) FROM {self.table_name};"
        count = pd.read_sql(query, conn)
        self.assertGreater(count.iloc[0, 0], 0, "No data stored in the table.")
