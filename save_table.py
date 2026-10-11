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

table_name = "4_player_holes"
input_file = "hole_odds/4_hole_odds.csv"
row_numbers = {
    "name": 0,
    "win_percent": 1,
    "draw_percent": None,
}
high_card_second = False


def get_id(high_card, low_card, modifier):
    if modifier == 'p':
        return 157+high_card
    else:
        if modifier == 'u':
            modifier_start = 0
        elif modifier== 's':
            modifier_start = 78

        row_start = high_card*(high_card-1)/2 + 1
        # print(f"id:{modifier_start+row_start+low_card}, row:{row_start}, top:{high_card}, low:{low_card}, mod:{modifier}")
        return modifier_start+row_start+low_card


with open(input_file, mode='r', newline='') as file:
    reader = csv.reader(file)

    for i, input_row in enumerate(reader):
        if i == 0:
            continue
        hole_name = ""
        modifier = "" # s:suited, u:unsuited, p:pair.

        win_percent = float(input_row[row_numbers["win_percent"]])
        if not row_numbers["draw_percent"] is None:
            win_percent += float(input_row[row_numbers["draw_percent"]])

        name_split = input_row[row_numbers["name"]].split(" ")
        
        if name_split[0] == "Pair":
            hole_name = f"{name_split[2][0]*2}"
            modifier = 'p'
        else:
            hole_name = f"{name_split[0][0]}{name_split[0][2]}"
            if name_split[1][0] == "s":
                modifier = 's'
            else:
                modifier = 'u'

        high_card = help.rank_values[hole_name[0]]
        low_card = help.rank_values[hole_name[1]]

        if high_card_second:
            low_card, high_card = high_card, low_card

        seperation = high_card-low_card
        if high_card == 12: # A
            seperation = min(seperation, low_card+1)
        
        if seperation < 5:
            connection = 5-seperation
        else:
            connection = 0

        id = get_id(high_card, low_card, modifier)

        sql = f"INSERT INTO `{table_name}` (`id`, `name`, `high_card`, `low_card`, `modifier`, `connection`, `win`) VALUES ({id}, '{hole_name}', {high_card}, {low_card}, '{modifier}', {connection}, {win_percent});"
        # print(sql)
        cursor.execute(sql)
        mydb.commit()

