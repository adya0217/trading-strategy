import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Make sure to import numpy

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",  # Replace with your actual password
    database="stock_data_db"
)

# Fetch all relevant stock data
query = "SELECT Datetime, Close, High, Low, Open, Volume, Instrument FROM stock_data ORDER BY Datetime"
df = pd.read_sql(query, db_connection)

# Close the database connection
db_connection.close()

# Set Datetime as index (assuming it is already in datetime format)
df.set_index('Datetime', inplace=True)

# Calculate short-term and long-term SMAs for the 'Close' prices
short_window = 20  # Short-term window
long_window = 50   # Long-term window

df['SMA20'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
df['SMA50'] = df['Close'].rolling(window=long_window, min_periods=1).mean()

# Generate signals based on SMA crossover
df['Signal'] = 0
df['Signal'][short_window:] = np.where(df['SMA20'][short_window:] > df['SMA50'][short_window:], 1, 0)  # Buy signal
df['Position'] = df['Signal'].diff()  # Buy (1) or Sell (-1)

# Plotting the stock prices along with SMAs
plt.figure(figsize=(14, 7))
plt.plot(df['Close'], label='Close Price', alpha=0.5)
plt.plot(df['SMA20'], label='20-Day SMA', alpha=0.75)
plt.plot(df['SMA50'], label='50-Day SMA', alpha=0.75)

# Plot buy signals
plt.plot(df[df['Position'] == 1].index, 
         df['SMA20'][df['Position'] == 1], 
         '^', markersize=10, color='g', label='Buy Signal')

# Plot sell signals
plt.plot(df[df['Position'] == -1].index, 
         df['SMA20'][df['Position'] == -1], 
         'v', markersize=10, color='r', label='Sell Signal')

plt.title('Stock Price and SMA Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
