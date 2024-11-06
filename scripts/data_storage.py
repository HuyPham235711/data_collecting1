import pandas as pd
import pyodbc
import os

#processed_data_path = os.path.join(".", "data", "processed", "TSLA1.csv")
#server = 'CAUBEKINH8\SQLEXPRESS'
#database = 'traday_TSLA'
#table_name = 'intraday_data_tsla'

def load_data(file_path):
    return pd.read_csv(file_path)

def connect_to_db(server, database):
    connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'

    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")
        return conn
    except pyodbc.Error as e:
        print("Error: ", e)
        return None

def insert_data(df, conn, table_name):
    cursor = conn.cursor()
    try:
        for index, row in df.iterrows():
            cursor.execute(f"""
                INSERT INTO {table_name} (open_price, high_price, low_price, close_price, volume)
                VALUES (?, ?, ?, ?, ?)
            """, row['open'], row['high'], row['low'], row['close'], row['volume'])
        conn.commit()
        print("Data inserted successfully!")
    except pyodbc.Error as e:
        print("Error: ", e)
    finally:
        cursor.close()

def store_data(processed_data_path, server, database, table_name):
    """Load data and insert into the specified SQL table."""
    df = load_data(processed_data_path)
    conn = connect_to_db(server, database)
    if conn:
        insert_data(df, conn, table_name)
        conn.close()
