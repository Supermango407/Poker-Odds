import help
import timeit
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

# sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `2_player_holes`;"
sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `2_player_holes` WHERE `modifier` LIKE 'u' AND `connection` < 2;"
# sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `2_player_holes` WHERE `modifier` NOT LIKE 'p'"
# sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `2_player_holes` WHERE `modifier` LIKE 'u';"

cursor.execute(sql)
card_table = cursor.fetchall()


# sliders_ranges = {
    # "percent_adder": np.arange(0, 5, 1),
    # "low_card_adder": np.arange(15, 25, 1),
    # "percent_offset": np.arange(10, 20, 1),
    # "high_card_multiplier": np.arange(1, 5, 1),
    # "low_card_multiplier":  np.arange(1, 2, 10),
    # "ace_adder":  np.arange(0.0, 5.0, 0.5),
    # "king_adder":  np.arange(0.0, 5.0, 0.5),
    # "queen_adder":  np.arange(0.0, 5.0, 0.5),
    # "connection_adder":  np.arange(5, 8, 0.5),
    # "connection_multiplier":  np.arange(0.0, 2.0, 0.5),
    # "suited_adder":  np.arange(2.6, 2.61, 0.1),
# }
sliders_ranges = {
    "percent_adder": np.arange(10, 20.5, 0.5),
    "card_adder": np.arange(0, 6, 1),
    "high_card_adder": np.arange(0, 10, 1),
    "12": np.arange(12, 20, 1),
    "11": np.arange(11, 17, 1),
    "10": np.arange(10, 15, 1),
    "9": np.arange(9, 12, 1),
    "8": np.arange(8, 10, 1),
    "7": np.arange(7, 9, 1),
    "6": np.arange(6, 8, 1),
    "5": np.arange(5, 7, 1),
    "4": np.arange(4, 6, 1),
    "3": np.arange(3, 5, 1),
    "2": np.arange(2, 4, 1),
    "1": np.arange(1, 3, 1),
    "0": np.arange(0, 1, 1),
}
range_keys = list(sliders_ranges.keys())


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
    percent_offset = sliders["percent_adder"]
    card_offset = sliders["percent_adder"]
    high_card_offset = sliders["high_card_adder"]
    # high_card_adder = sliders["high_card_adder"]
    # low_card_adder = sliders["low_card_adder"]
    # high_card_multiplier = sliders["high_card_multiplier"]
    # low_card_multiplier = sliders["low_card_multiplier"]
    # ace_adder = sliders["ace_adder"]
    # king_adder = sliders["king_adder"]
    # queen_adder = sliders["queen_adder"]
    
    rank_offsets = [
        sliders["0"],
        sliders["1"],
        sliders["2"],
        sliders["3"],
        sliders["4"],
        sliders["5"],
        sliders["6"],
        sliders["7"],
        sliders["8"],
        sliders["9"],
        sliders["10"],
        sliders["11"],
        sliders["12"],
    ]

    estimation = percent_offset

    estimation += rank_offsets[high_card]+card_offset+high_card_offset
    estimation += rank_offsets[low_card]+card_offset
    # estimation += (high_card+high_card_adder)*high_card_multiplier
    # estimation += (low_card+low_card_adder)*low_card_multiplier
    # estimation += (connection+connection_adder) * connection_multiplier

    # if high_card == 12:
    #     estimation += ace_adder
    # elif high_card == 11:
    #     estimation += king_adder
    # elif high_card == 10:
    #     estimation += queen_adder

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

    for row in card_table:
        id, name, high_card, low_card, modifier, connection, win_percent  = row
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


def calculate_best_estimate(ranges, sliders={}, current_best=math.inf, best_sliders=None, slider_index=0):
    slider_name = range_keys[slider_index]
    current_range = ranges[slider_name]
    last_slider = len(ranges) == slider_index+1
    for i, slider_value in enumerate(current_range):
        current_slider = sliders.copy()
        current_slider[slider_name] = slider_value

        if slider_index == 0:
            print(f"{i}/{len(current_range)}")
        elif slider_index == 1:
            print(f"---{i}/{len(current_range)}")

        if last_slider:
            calculate_error(current_slider)
            error = total_error_abs
            if error < current_best:
                current_best = error
                best_sliders = current_slider
        else:
            (current_best, best_sliders) = calculate_best_estimate(ranges, current_slider, current_best, best_sliders, slider_index+1)

    return (current_best, best_sliders)


def print_and_estimate():
    print()
    total = len(card_table)
    print(f"cards: {len(card_table)}")
    for slider_name in sliders_ranges:
        slider_value = sliders_ranges[slider_name]
        total *= len(slider_value)
        print(f"{slider_name}: {len(slider_value)}")
    print(f"total: {total:,}")
    print(f"ETA: {total*0.0000358613}")
    print()
    
    error, sliders = calculate_best_estimate(sliders_ranges)
    print()
    print(f"{error:.4f}")

    print()
    for slider_name in sliders:
        slider_value = sliders[slider_name]
        print(f'"{slider_name}": np.{slider_value.dtype}({slider_value}),')
    print()

    # return None

    # calculate_error(sliders, print_rows=True, save=True)


print_and_estimate()

# calculate_error({
#     "high_card_adder": np.int64(0),
#     "low_card_adder": np.int64(15),
#     "percent_offset": np.int64(13),
#     "high_card_multiplier": np.int64(2),
#     "low_card_multiplier": np.int64(1),
#     "ace_adder": np.float64(3.5),
#     "king_adder": np.float64(2.5),
#     "queen_adder": np.float64(1.5),
# },print_rows=True, save=True)

# calculate_error({
#     "percent_adder": np.float64(13.0),
#     "card_adder": np.int64(0),
#     "12": np.int64(12),
#     "11": np.int64(11),
#     "10": np.int64(10),
#     "9": np.int64(9),
#     "8": np.int64(8),
#     "7": np.int64(7),
#     "6": np.int64(6),
#     "5": np.int64(5),
#     "4": np.int64(4),
#     "3": np.int64(3),
#     "2": np.int64(2),
#     "1": np.int64(1),
#     "0": np.int64(0),
# },print_rows=True, save=True)

# func = lambda: calculate_error({
#     "percent_adder": np.float64(13.0),
#     "card_adder": np.int64(0),
#     "12": np.int64(12),
#     "11": np.int64(11),
#     "10": np.int64(10),
#     "9": np.int64(9),
#     "8": np.int64(8),
#     "7": np.int64(7),
#     "6": np.int64(6),
#     "5": np.int64(5),
#     "4": np.int64(4),
#     "3": np.int64(3),
#     "2": np.int64(2),
#     "1": np.int64(1),
#     "0": np.int64(0),
# })

# number = 1000000
# time = timeit.timeit(func, number=number)
# print(f"total:{time:.6}, average:{time/number:.6}")
# # total:36.7625221000053, average:3.6762522100005297e-05 (36.76 microseconds)
