import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(user="osuadmin",
                                password=os.environ.get('password'),
                                host="software-quiz.mysql.database.azure.com",
                                port=3306, database="quiz")

    def execute(self, command, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute(command, data)
            return cursor
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
