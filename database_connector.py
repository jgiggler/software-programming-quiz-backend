import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    """
    Initializes MySQL server connection, runs SQL command, and closes server connection.
    """
    def __init__(self):
        self.connection = mysql.connector.connect(user="osuadmin",
                                password=os.environ.get('password'),
                                host="software-quiz.mysql.database.azure.com",
                                port=3306, database="quiz")

    def execute(self, command, data):
        if self.connection is None:
            print("Cannot execute query: Database connection was not initialized!")
            return
        if command is None or len(command.strip()) == 0:
            print("Cannot execute query: Invalid query provided!")
            return
        cursor = self.connection.cursor()

        # Insert data with SQL command
        cursor.execute(command, data)

        # Make sure data is committed to the database
        self.connection.commit()
        return cursor

    def close(self):
        self.connection.close()
