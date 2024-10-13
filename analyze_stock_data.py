import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 


db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql", 
    database="stock_data_db"
)


query = "SELECT Datetime, Close, High, Low, Open, Volume, Instrument FROM stock_data ORDER BY Datetime"
df = pd.read_sql(query, db_connection)


db_connection.close()


df.set_index('Datetime', inplace=True)


short_window = 20 
long_window = 50  

df['SMA20'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
df['SMA50'] = df['Close'].rolling(window=long_window, min_periods=1).mean()


df['Signal'] = 0
df['Signal'][short_window:] = np.where(df['SMA20'][short_window:] > df['SMA50'][short_window:], 1, 0) 
df['Position'] = df['Signal'].diff() 


plt.figure(figsize=(14, 7))
plt.plot(df['Close'], label='Close Price', alpha=0.5)
plt.plot(df['SMA20'], label='20-Day SMA', alpha=0.75)
plt.plot(df['SMA50'], label='50-Day SMA', alpha=0.75)


plt.plot(df[df['Position'] == 1].index, 
         df['SMA20'][df['Position'] == 1], 
         '^', markersize=10, color='g', label='Buy Signal')


plt.plot(df[df['Position'] == -1].index, 
         df['SMA20'][df['Position'] == -1], 
         'v', markersize=10, color='r', label='Sell Signal')

plt.title('Stock Price and SMA Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
