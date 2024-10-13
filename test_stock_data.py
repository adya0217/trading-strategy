import mysql.connector
import unittest
from datetime import datetime
from decimal import Decimal

class TestStockData(unittest.TestCase):

    def setUp(self):
        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="stock_data_db"
        )
        self.cursor = self.db_connection.cursor()

    def tearDown(self):
        # Close the database connection after each test
        self.cursor.close()
        self.db_connection.close()

    def test_data_validity(self):
        # Fetch data from MySQL
        self.cursor.execute("SELECT Datetime,Close,High,Low,Open,Volume,Instrument FROM stock_data")
        data = self.cursor.fetchall()

        for row in data:
            self.assertIsInstance(row[0], datetime, "Date should be in valid datetime format")
            self.assertIsInstance(row[1], Decimal, "Close should be a Decimal")
            self.assertIsInstance(row[2], Decimal, "High should be a Decimal")
            self.assertIsInstance(row[3], Decimal, "Low should be a Decimal")
            self.assertIsInstance(row[4], Decimal, "Open should be a Decimal")
            self.assertIsInstance(row[5], int, "Volume should be an integer")
            self.assertIsInstance(row[6], str, "Instrument should be a string")
    
        
if __name__ == '__main__':
    unittest.main()
