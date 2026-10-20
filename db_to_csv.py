import help
import mysql.connector
import csv

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="poker"
)
cursor = mydb.cursor(buffered=True)

table_index = "10"
output_file = f"table_save/{table_index}_holes_save.csv"

sql = f"SELECT * FROM `{table_index}_player_holes` ORDER BY `top` ASC;"
cursor.execute(sql)

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([column[0] for column in cursor.description])
    writer.writerows(cursor.fetchall())

cursor.close()
mydb.close()


