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
sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u' AND `connection` < 2;"
# sql = "SELECT * FROM `2_player_holes` WHERE `modifier` NOT LIKE 'p'"
# sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u';"

cursor.execute(sql)
table = cursor.fetchall()


sliders_ranges = [
    ("high_card_adders", np.arange(0, 5, 1)),
    ("low_card_adders", np.arange(15, 25, 1)),
    ("percent_offsets", np.arange(10, 20, 1)),
    ("high_card_multipliers", np.arange(1.5, 2, 0.25)),
    ("low_card_multipliers",  np.arange(1, 2, 10)),
    ("ace_adder",  np.arange(2.0, 5.0, 0.5)),
    ("king_adder",  np.arange(2.0, 5.0, 0.5)),
    ("queen_adder",  np.arange(2.0, 5.0, 0.5)),
    # ("connection_adder",  np.arange(5, 8, 0.5)),
    # ("connection_multiplier",  np.arange(0.0, 2.0, 0.5)),
    # ("suited_adder",  np.arange(2.6, 2.61, 0.1)),
]


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


def estimate_hand(high_card, low_card, modifier, connection, sliders):
    high_card_adder = sliders[0][1]
    low_card_adder = sliders[1][1]
    percent_offset = sliders[2][1]
    high_card_multiplier = sliders[3][1]
    low_card_multiplier = sliders[4][1]
    ace_adder = sliders[5][1]
    king_adder = sliders[6][1]
    queen_adder = sliders[7][1]
    # connection_adder = sliders[7][1]
    # connection_multiplier = sliders[8][1]
    # suited_adder = sliders[9][1]
    
    estimation = percent_offset
    estimation += (high_card+high_card_adder)*high_card_multiplier
    estimation += (low_card+low_card_adder)*low_card_multiplier
    # estimation += (connection+connection_adder) * connection_multiplier

    if high_card == 12:
        estimation += ace_adder
    elif high_card == 11:
        estimation += king_adder
    elif high_card == 1:
        estimation += queen_adder

    # if modifier == 's':
        # if estimation > 55:
        #     estimation += -0.5
        # elif estimation < 45:
        #     estimation += 0.5
        # estimation += suited_adder
    # elif modifier == 'p':
    #     estimation *= pair_multiplier

    return estimation


def calculate_error(sliders, print_rows=False, save=False):
    global total_error, total_error_abs, squared_error, max_error

    if save:
        cursor.execute("TRUNCATE `2_player_estimate`")
        mydb.commit()

    # Reset error values
    total_error = 0
    total_error_abs = 0
    squared_error = 0
    max_error = 0

    for row in table:
        id, name, high_card, low_card, modifier, connection, win_percent = row
        estimate = estimate_hand(high_card, low_card, modifier, connection, sliders)
        error = win_percent - estimate
        total_error += error
        total_error_abs += abs(error)
        squared_error += error ** 2
        
        if abs(error) > max_error:
            max_error = abs(error)

        if print_rows:
            print(f"{name} {modifier}: {error:5.2f}, {error*error:5.2f}")
        if save:
            sql = f"INSERT INTO `2_player_estimate` (`id`, `name`, `high_card`, `low_card`, `modifier`, `connection`, `win`, `estimate`, `abs_error`, `error`) VALUES ({id}, '{name}', {high_card}, {low_card}, '{modifier}', {connection}, {win_percent:5.2f}, {estimate:5.2f}, {abs(error):5.2f}, {error:5.2f});"
            cursor.execute(sql)
            mydb.commit()

    if print_rows:
        print()
        print(f"total: {total_error_abs:6.2f}, {total_error:6.2f}")
        print(f"squared: {squared_error:6.2f}")
        print(f"max: {max_error:6.2f}")


def calculate_best_estimate(ranges, sliders=[], current_best=math.inf, best_sliders=None, slider_index=0):
    current_range = ranges[slider_index][1]
    slider_name = ranges[slider_index][0]
    last_slider = len(ranges) == slider_index+1
    for i, current_slider in enumerate(current_range):
        current_sliders = sliders+[(slider_name, current_slider)]
        if slider_index == 0:
            print(f"{i}/{len(current_range)}")
        elif slider_index == 1:
            print(f"---{i}/{len(current_range)}")

        if last_slider:
            calculate_error(current_sliders)
            error = squared_error
            if error < current_best:
                current_best = error
                best_sliders = current_sliders
        else:
            (current_best, best_sliders) = calculate_best_estimate(ranges, current_sliders, current_best, best_sliders, slider_index+1)

    return (current_best, best_sliders)


# error, sliders = calculate_best_estimate(sliders_ranges)
# print()
# print(error)
# print()
# for slider in sliders:
#     print(f"{slider},")
# print()


calculate_error([
    ('high_card_adders', np.int64(2)),
    ('low_card_adders', np.int64(15)),
    ('percent_offsets', np.int64(12)),
    ('high_card_multipliers', np.float64(1.75)),
    ('low_card_multipliers', np.int64(1)),
    ('ace_adder', np.float64(4.0)),
    ('king_adder', np.float64(2.5)),
    ('queen_adder', np.float64(2.0)),
],print_rows=True, save=True)


# total = 1
# for slider in sliders_ranges:
#     total *= len(slider[1])
#     print(f"{slider[0]}: {len(slider[1])}")
# print(total)

