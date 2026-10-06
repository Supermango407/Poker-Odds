import help
import math
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)
cursor = mydb.cursor(buffered=True)

# sql = "SELECT * FROM `2_player_holes`;"
sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u' AND `connection` < 4;"
# sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u';"

cursor.execute(sql)
table = cursor.fetchall()


high_card_adders = np.arange(0, 20, 1)
low_card_adders = np.arange(0, 20, 1)
percent_offsets = np.arange(0, 10, 0.5)
high_card_multipliers = np.arange(1, 2, 0.25)
low_card_multipliers =  np.arange(1, 2, 1)
# pair_multiplier = 1.333333333
# suited_adder = 2
# connection_adder = 0
# connection_multiplier = 0

total_error = 0
total_error_abs = 0
squared_error = 0
max_error = 0

unsuited_error = 0
unsuited_error_abs = 0

suited_error = 0
suited_error_abs = 0

paired_error = 0
paired_error_abs = 0


def estimate_hand(high_card, low_card, modifier, connection, high_card_adder, low_card_adder, percent_offset, high_card_multiplier, low_card_multiplier):
    estimation = (high_card+high_card_adder)*high_card_multiplier
    estimation += (low_card+low_card_adder)*low_card_multiplier

    # if modifier == 's':
    #     estimation += suited_adder
    # elif modifier == 'p':
    #     estimation *= pair_multiplier

    # estimation += (connection+connection_adder) * connection_multiplier

    estimation += percent_offset

    return estimation


def calculate_error(high_card_adder, low_card_adder, percent_adder, high_card_multiplier, low_card_multiplier, print_rows=False):
    global total_error, total_error_abs, squared_error, max_error

    # Reset error values
    total_error = 0
    total_error_abs = 0
    squared_error = 0
    max_error = 0

    for row in table:
        id, name, high_card, low_card, modifier, connection, win_percent, lose_percent, draw_percent = row
        estimate = estimate_hand(high_card, low_card, modifier, connection, high_card_adder, low_card_adder, percent_adder, high_card_multiplier, low_card_multiplier)
        error = win_percent+draw_percent - estimate
        total_error += error
        total_error_abs += abs(error)
        squared_error += error ** 2
        
        if abs(error) > max_error:
            max_error = abs(error)

        if print_rows:
            print(f"{name} {modifier}: {error:5.2f}, {error*error:5.2f}")


def calculate_best_estimate():
    current_best = math.inf
    best_values = {"high_card_adder": None, "low_card_adder": None, "percent_adder": None, "high_card_multiplier": None, "low_card_multiplier": None}
    i_length = len(high_card_adders)
    j_length = len(low_card_adders)

    for i, high_card_adder in enumerate(high_card_adders):
        print(f"{i}/{i_length}")
        for j, low_card_adder in enumerate(low_card_adders):
            # print(f"  {j}/{j_length}")

            for percent_offset in percent_offsets:
                for high_card_multiplier in high_card_multipliers:
                    for low_card_multiplier in low_card_multipliers:
                        calculate_error(high_card_adder, low_card_adder, percent_offset, high_card_multiplier, low_card_multiplier, print_rows=False)
                        error = squared_error  # You can choose to use total_error_abs, squared_error, or max_error as the metric for comparison
                        if error < current_best:
                            current_best = error
                            best_values["high_card_adder"] = high_card_adder
                            best_values["low_card_adder"] = low_card_adder
                            best_values["percent_adder"] = percent_offset
                            best_values["high_card_multiplier"] = high_card_multiplier
                            best_values["low_card_multiplier"] = low_card_multiplier

    print()
    print(f"error: {current_best}")
    for key in best_values:
        print(f"{key}: {best_values[key]}")
    
    return best_values


# calculate_best_estimate()

calculate_error(
    high_card_adder=3,
    low_card_adder=17,
    percent_adder=9.5,
    high_card_multiplier=1.75,
    low_card_multiplier=1.0,
    print_rows=True
)

# print()
# print(f"total: {total_error_abs:6.2f}, {total_error:6.2f}")
# print(f"squared: {squared_error:6.2f}")
# print(f"max: {max_error:6.2f}")
