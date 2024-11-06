CREATE TABLE intraday_data_tsla (
    id INT PRIMARY KEY IDENTITY(1,1),  -- Optional: Auto-incrementing primary key
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume INT
);
