import dbmanager
import mysql.connector

# inittialize the database connection
connection = dbmanager.init_connection()

# execute sql cmd
cursor = connection.cursor()
cursor.execute('SELECT * FROM starbucks')

# store results in a variable
results = cursor.fetchall()

print(results)
