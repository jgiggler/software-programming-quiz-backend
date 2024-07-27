import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(user=os.getenv('user'),
                                password=os.getenv('password'),
                                host=os.getenv('host'),
                                port=3306, database="quiz")
    def execute(self, command, data):
        """
        Run SQL command on provided data and returns cursor
        """
        if command is None or len(command.strip()) == 0:
            print("Cannot execute query: Invalid query provided!")
            return
        # Instantiate a MySQLCursor object: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-constructor.html
        cursor = self.connection.cursor()
        # Run SQL command: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        cursor.execute(command, data)
        return cursor

    def close(self):
        """
        Disconnects SQL connection: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-close.html
        """
        self.connection.close()

    def commit(self):
        """
        Make sure data is committed to the database: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-commit.html
        """
        self.connection.commit()
