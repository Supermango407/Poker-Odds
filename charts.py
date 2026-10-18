import matplotlib.pyplot as plt
import mysql.connector
import math
import numpy as np


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)
cursor = mydb.cursor(buffered=True)

tables = {}
for i in range(2, 5):
    sql = f"SELECT `id`, `win`, `rarity`, `top` FROM `{i}_player_holes` ORDER BY `top`;"
    cursor.execute(sql)
    tables[i] = cursor.fetchall()

table_len = len(tables[2])

win_list_2 = []
win_list_3 = []
win_list_4 = []
top_list = []

win_max_2 = tables[2][0][1]
win_max_3 = tables[3][0][1]
win_max_4 = tables[4][0][1]
win_min_2 = tables[2][-1][1]
win_min_3 = tables[3][-1][1]
win_min_4 = tables[4][-1][1]

for row in tables[2]:
    _, win, rarity, top = row
    win_list_2.append(tables[2][top-1][1])
    win_list_3.append(tables[3][top-1][1])
    win_list_4.append(tables[4][top-1][1])
    # win_list_2.append((tables[2][top-1][1]-win_min_2)/(win_max_2-win_min_2))
    # win_list_3.append((tables[3][top-1][1]-win_min_3)/(win_max_3-win_min_3))
    # win_list_4.append((tables[4][top-1][1]-win_min_4)/(win_max_4-win_min_4))
    top_list.append(top)

plt.plot(top_list, win_list_2, marker='.', label="2 players")
plt.plot(top_list, win_list_3, marker='.', label="3 players")
plt.plot(top_list, win_list_4, marker='.', label="4 players")
plt.title("Poker Odds")
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(table_len, 0)
plt.show()
