import mysql.connector
import csv
import os

print("Current Working Directory:", os.getcwd())


conn = mysql.connector.connect(
    host="localhost",       
    user="root",            
    password="mysql",
    database="stock_data_db" 
)


cursor = conn.cursor()


sql = """
    INSERT INTO stock_data (Datetime,Close,High,Low,Open,Volume,Instrument)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""


with open('C:/Users/Adya/PythonTesting/stock_data.csv', 'r') as csvfile:

    reader = csv.reader(csvfile)
    next(reader) 
    
 
    for row in reader:
        cursor.execute(sql, tuple(row))


cursor.close()
conn.close()

print("Data inserted successfully.")
