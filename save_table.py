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

input_file = "hole_odds/hole_odds_2.csv"


def get_id(high_card, low_card, modifier):
    if modifier == 'p':
        return 157+high_card
    else:
        if modifier == 'u':
            modifier_start = 0
        elif modifier== 's':
            modifier_start = 78

        row_start = high_card*(high_card-1)/2 + 1
        return modifier_start+row_start+low_card


with open(input_file, mode='r', newline='') as file:
    reader = csv.reader(file)

    for i, input_row in enumerate(reader):
        hole_name = ""
        modifier = "" # s:suited, u:unsuited, p:pair.

        win_percent = float(input_row[1])
        lose_percent = float(input_row[2])
        draw_percent = float(input_row[3])

        name_split = input_row[0].split(" ")
        
        if name_split[0] == "Pair":
            hole_name = f"{name_split[2][0]*2}"
            modifier = 'p'
        else:
            hole_name = f"{name_split[0][0]}{name_split[0][2]}"
            if name_split[1][0] == "s":
                modifier = 's'
            else:
                modifier = 'u'

        high_card = help.rank_values[hole_name[1]]
        low_card = help.rank_values[hole_name[0]]
        seperation = high_card-low_card
        if high_card == 12: # A
            seperation = min(seperation, low_card+1)
        if seperation < 5:
            connected = 5-seperation
        else:
            connected = 0

        id = get_id(high_card, low_card, modifier)

        sql = f"INSERT INTO `2_player_holes` (`id`, `name`, `high_card`, `low_card`, `modifier`, `separation`, `win`, `lose`, `draw`) VALUES ({id}, '{hole_name}', {high_card}, {low_card}, '{modifier}', '{seperation}', {win_percent}, '{lose_percent}', '{draw_percent}');"
        # print(sql)
        cursor.execute(sql)
        mydb.commit()

