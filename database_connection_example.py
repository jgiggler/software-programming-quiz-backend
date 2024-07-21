import mysql.connector

cnx = mysql.connector.connect(user="osuadmin", password="", host="software-quiz.mysql.database.azure.com", port=3306, database="quiz", ssl_ca="{ca-cert filename}", ssl_disabled=False)
cursor = cnx.cursor()

add_employer = ("INSERT INTO employer "
               "(Email, Password) "
               "VALUES (%s, %s)")

data_employer = ('Geert', 'Vanderkelen')

# Insert data with SQL command
cursor.execute(add_employer, data_employer)

# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()