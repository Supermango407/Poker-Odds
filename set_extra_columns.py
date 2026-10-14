import help
import mysql.connector
import csv

table_name = "4_player_holes"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="poker"
)
cursor = mydb.cursor(buffered=True)

sql = f"SELECT `id`, `modifier`, `win` FROM `{table_name}` ORDER BY `win` DESC"
cursor.execute(sql)
card_table = cursor.fetchall()

rarity = 0.0
for i, hole in enumerate(card_table):
    id, modifier, _ = hole
    chance = 0.0
    if modifier == 'u':
        chance = 24/2652
    elif modifier == 's':
        chance = 8/2652
    elif modifier == 'p':
        chance = 12/2652
    else:
        raise TypeError("Modifier Error")
    rarity += chance
    
    sql = f"UPDATE `{table_name}` SET `chance` = '{chance*100:.3f}', `rarity` = '{rarity*100:.3f}', `top` = '{i+1}' WHERE `{table_name}`.`id` = {id};"
    cursor.execute(sql)

mydb.commit()
