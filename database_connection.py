import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="management"
)

cursor = database.cursor()
