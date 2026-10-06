import help
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)
cursor = mydb.cursor(buffered=True)


card_offset = 13
percent_offset = 0
high_card_multiplier = 1.75
low_card_multiplier = 1.0
pair_multiplier = 1.333333333
suited_adder = 2
connection_adder = 0
connection_multiplier = 0

sql = "SELECT * FROM `2_player_holes` ORDER BY `2_player_holes`.`id` ASC;"
cursor.execute(sql)
table = cursor.fetchall()

total_error = 0
total_error_abs = 0

unsuited_error = 0
unsuited_error_abs = 0

suited_error = 0
suited_error_abs = 0

paired_error = 0
paired_error_abs = 0


for row in table:
    id, name, high_card, low_card, modifier, separation, win_percent, lose_percent, draw_percent = row
    print(name, modifier, high_card, low_card, separation, win_percent, lose_percent, draw_percent)


# print(f"total: {total_error_abs:6.2f}, {total_error:6.2f}")
# print(f"unsuited: {unsuited_error_abs:6.2f}, {unsuited_error:6.2f}")
# print(f"suited: {suited_error_abs:6.2f}, {suited_error:6.2f}")
# print(f"paired: {paired_error_abs:6.2f}, {paired_error:6.2f}")

