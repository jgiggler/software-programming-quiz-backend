import mysql.connector
import os

def connect(command, data):
    """
    Initializes MySQL server connection, runs SQL command, and closes server connection.
    """
    cnx = mysql.connector.connect(user="osuadmin", password=os.environ.get('password'), host="software-quiz.mysql.database.azure.com", port=3306, database="{your_database}", ssl_ca="{ca-cert filename}", ssl_disabled=False)
    cursor = cnx.cursor()

    # Insert data with SQL command
    cursor.execute(command, data)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()