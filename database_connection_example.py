import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

cnx = mysql.connector.connect(user="osuadmin", password=os.getenv('password'), host="software-quiz.mysql.database.azure.com", port=3306, database="quiz")
cursor = cnx.cursor()

add_employer = ("INSERT INTO employer "
               "(Email, Password) "
               "VALUES (%s, %s)")

data_employer = ('Geegee3', 'Vanderkelen')

# Insert data with SQL command
cursor.execute(add_employer, data_employer)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()