import help
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)
cursor = mydb.cursor(buffered=True)

# sql = "SELECT * FROM `2_player_holes`;"
sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u' AND `connection` = 0;"
# sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u';"

cursor.execute(sql)
table = cursor.fetchall()


card_offset = 15
percent_offset = 2
high_card_multiplier = 1.75
low_card_multiplier = 1.0
pair_multiplier = 1.333333333
suited_adder = 2
connection_adder = 0
connection_multiplier = 0

total_error = 0
total_error_abs = 0

unsuited_error = 0
unsuited_error_abs = 0

suited_error = 0
suited_error_abs = 0

paired_error = 0
paired_error_abs = 0


def estimate_hand(high_card, low_card, modifier, connection):
    estimation = (high_card+card_offset)*high_card_multiplier
    estimation += (low_card+card_offset)*low_card_multiplier

    if modifier == 's':
        estimation += suited_adder
    elif modifier == 'p':
        estimation *= pair_multiplier

    estimation += (connection+connection_adder) * connection_multiplier

    estimation += percent_offset

    return estimation


def calculate_error():
    global total_error, total_error_abs, unsuited_error, unsuited_error_abs, suited_error, suited_error_abs, paired_error, paired_error_abs
    
    for row in table:
        id, name, high_card, low_card, modifier, connection, win_percent, lose_percent, draw_percent = row
        estimate = estimate_hand(high_card, low_card, modifier, connection)
        error = win_percent+draw_percent - estimate
        print(f"{name} {modifier}: {error}")

        total_error += error
        total_error_abs += abs(error)

        if modifier == 'u':
            unsuited_error += error
            unsuited_error_abs += abs(error)
        elif modifier == 's':
            suited_error += error
            suited_error_abs += abs(error)
        elif modifier == 'p':
            paired_error += error
            paired_error_abs += abs(error)


calculate_error()

print()
print(f"total: {total_error_abs:6.2f}, {total_error:6.2f}")
# print(f"unsuited: {unsuited_error_abs:6.2f}, {unsuited_error:6.2f}")
# print(f"suited: {suited_error_abs:6.2f}, {suited_error:6.2f}")
# print(f"paired: {paired_error_abs:6.2f}, {paired_error:6.2f}")

