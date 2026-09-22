import mysql.connector
import help

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)

cursor = mydb.cursor(buffered=True)
