from help import ranks
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


table_indices = [
    "02",
    "03",
    "04",
    "06",
    "08",
    "10",
]


def show_table():
    tables = {}
    for index in table_indices:
        sql = f"SELECT `id`, `modifier`, `win`, `rarity`, `top` FROM `{index}_player_holes` ORDER BY `top`;"
        cursor.execute(sql)
        tables[index] = cursor.fetchall()


    table = tables[table_indices[0]]
    table_len = len(table)

    top_hands = {}
    top_unsuited = {}
    top_suited = {}
    top_pairs = {}

    hands = {}
    unsuited = {}
    suited = {}
    pairs = {}


    for players in table_indices:
        top_hands[players] = []
        top_unsuited[players] = []
        top_suited[players] = []
        top_pairs[players] = []

        hands[players] = []
        unsuited[players] = []
        suited[players] = []
        pairs[players] = []

        for row in tables[players]:
            id, modifier, win, rarity, top = row
            value = win
            if modifier == 'u':
                unsuited[players].append(value)
                top_unsuited[players].append(top)
            elif modifier == 's':
                suited[players].append(value)
                top_suited[players].append(top)
            elif modifier == 'p':
                pairs[players].append(value)
                top_pairs[players].append(top)
            else:
                raise ValueError("No Modifier Found")
            
            hands[players].append(value)
            top_hands[players].append(top)


    for players in table_indices:
        # plt.plot(top_hands[players], hands[players], marker='.', label=f"{players} hands")
        plt.plot(top_pairs[players], pairs[players], marker='.', label=f"{players} pairs")
        plt.plot(top_suited[players], suited[players], marker='.', label=f"{players} suited")
        plt.plot(top_unsuited[players], unsuited[players], marker='.', label=f"{players} unsuited")


def show_hole(name, modifier):
    holes = []
    players = []
    for index in table_indices:
        sql = f'SELECT `id`, `name`, `modifier`, `win`, `rarity`, `top` FROM `{index}_player_holes` WHERE `name` = "{name}" AND `modifier` = "{modifier}";'
        cursor.execute(sql)
        id, _, _,  win, rarity, top = cursor.fetchone()
        
        holes.append(100-rarity)
        players.append(int(index))

    plt.plot(players, holes, marker='.', label=f"{name} {modifier} odds")
    plt.ylim(0, 100)


# for rank in ranks:
#     show_hole(f"{rank}{rank}", 'p')

if True:
    user_input = input()
    show_hole(user_input[0:2].upper(), user_input[-1].lower())

plt.title("Poker Odds")
plt.legend()
plt.minorticks_on()
plt.grid(which="major", linewidth=1, alpha=1)
plt.grid(which="minor", linewidth=0.5, alpha=0.5)
plt.show()
