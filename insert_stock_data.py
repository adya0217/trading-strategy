import mysql.connector
import csv
import os

print("Current Working Directory:", os.getcwd())

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",        # Your MySQL host
    user="root",             # Your MySQL username
    password="mysql",# Your MySQL password
    database="stock_data_db" # The database you created
)

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Define the SQL query for inserting data
sql = """
    INSERT INTO stock_data (Datetime,Close,High,Low,Open,Volume,Instrument)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# Step 4: Read data from the CSV file
with open('C:/Users/Adya/PythonTesting/stock_data.csv', 'r') as csvfile:

    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    
    # Step 5: Insert each row into the database
    for row in reader:
        cursor.execute(sql, tuple(row))

# Step 6: Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")
