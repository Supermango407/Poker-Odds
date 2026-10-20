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

# sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `02_player_holes` WHERE `modifier` LIKE 'u' AND `connection` < 2;"
# sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `02_player_holes` WHERE `modifier` LIKE 'u';"
# sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `02_player_holes` WHERE `modifier` NOT LIKE 'p'"
sql = "SELECT `id`,`name`,`high_card`,`low_card`,`modifier`,`connection`,`win` FROM `02_player_holes`;"

cursor.execute(sql)
card_table = cursor.fetchall()


# sliders_ranges = {
#     "percent_adder": np.arange(50, 15, -1),
#     "low_card_adder": np.arange(-5, 5, 1),
#     "high_card_adder": np.arange(0, 25, 1),
#     "rank_multiplier": np.arange(1, 5, 1),
#     "rank_invert": [True, False],
#     "connection_multiplier": np.arange(0, 10, 100),
#     "connection_invert": [False],
#     "ace_adder": np.arange(6, 10, 1),
#     "king_adder": np.arange(5, 7, 1),
#     "queen_adder": np.arange(4, 6, 1),
#     "jack_adder": np.arange(2, 3, 1),
#     "10_adder": np.arange(2, 4, 1),
# }

slider_steps = {
    "card_adder": (np.float64(2.00), 0),
    "percent_adder": (np.float64(22.00), 1),
    "pair_adder": (np.float64(27.00), 1),
    "pair_scaler": (np.float64(1.50), 0.5),
    "high_card_scaler": (np.float64(1.00), 0),
    "low_card_scaler": (np.float64(0.00), 0),
    "connection_scaler": (np.float64(0.00), 0.0),
    "suited_adder": (np.float64(2.50), 0.5),
    "adjacent_adder_4": (np.float64(2.50), 0),
    "adjacent_adder_3": (np.float64(2.00), 0),
    "adjacent_adder_2": (np.float64(1.00), 0),
    "adjacent_adder_1": (np.float64(0.50), 0),
    "ace_adder": (np.float64(1.50), 0.5),
    "king_adder": (np.float64(1.00), 0.5),
    "queen_adder": (np.float64(0.50), 0.5),
    "jack_adder": (np.float64(0.00), 0),
    "10_adder": (np.float64(0.00), 0),
}
range_keys = list(slider_steps.keys())


total_error = 0
total_error_abs = 0
squared_error = 0
max_error = 0

def scaler_to_multiplier(value):
    if value < 0:
        return -1/(value-1)
    else:
        return value+1


def get_rank_number(rank, sliders):
    if rank < 8:
        return rank
    elif rank == 8:
        return rank + sliders["10_adder"]
    elif rank == 9:
        return rank + sliders["jack_adder"]
    elif rank == 10:
        return rank + sliders["queen_adder"]
    elif rank == 11:
        return rank + sliders["king_adder"]
    elif rank == 12:
        return rank + sliders["ace_adder"]
    else:
        raise ValueError(f"Invalid rank: {rank}")


def estimate_hand(high_card, low_card, modifier, connection, sliders):
    card_adder = sliders["card_adder"]
    percent_adder = sliders["percent_adder"]
    pair_adder = sliders["pair_adder"]
    pair_multiplier = scaler_to_multiplier(sliders["pair_scaler"])
    high_card_multiplier = scaler_to_multiplier(sliders["high_card_scaler"])
    low_card_multiplier = scaler_to_multiplier(sliders["low_card_scaler"])
    connection_multiplier = scaler_to_multiplier(sliders["connection_scaler"])
    # adjacent_adder = sliders["adjacent_adder"]
    suited_adder = sliders["suited_adder"]

    estimation = percent_adder

    if modifier == 'p':
        estimation += pair_adder
        estimation += pair_multiplier*(get_rank_number(high_card, sliders)+card_adder)
    else:
        estimation += high_card_multiplier*(get_rank_number(high_card, sliders)+card_adder)
        estimation += low_card_multiplier*(get_rank_number(low_card, sliders)+card_adder)

        if connection > 0:
            estimation += sliders[f"adjacent_adder_{connection}"]*connection_multiplier

        if modifier == 's':
            # if estimation > 55:
            #     estimation += -0.5
            # elif estimation < 45:
            #     estimation += 0.5
            estimation += suited_adder

    return estimation


def calculate_error(sliders, print_rows=False, save=False, min_error=math.inf):
    global total_error, total_error_abs, squared_error, max_error

    if save:
        cursor.execute("TRUNCATE `02_player_estimate`")
        mydb.commit()

    # Reset error values
    total_error = 0
    total_error_abs = 0
    squared_error = 0
    max_error = 0

    for row in card_table:
        id, name, high_card, low_card, modifier, connection, win_percent  = row
        estimate = estimate_hand(high_card, low_card, modifier, connection, sliders)
        error =  estimate - win_percent
        total_error += error
        total_error_abs += abs(error)
        squared_error += error ** 2

        if total_error_abs > min_error:
            return "error_exceeded"
        
        if abs(error) > max_error:
            max_error = abs(error)
            # if max_error > min_error:
            #     return "error_exceeded"

        if print_rows:
            print(f"{name} {modifier}: {error:5.2f}, {error*error:5.2f}")
        if save:
            sql = f"INSERT INTO `02_player_estimate` (`id`, `name`, `high_card`, `low_card`, `modifier`, `connection`, `win`, `estimate`, `abs_error`, `error`) VALUES ({id}, '{name}', {high_card}, {low_card}, '{modifier}', {connection}, {win_percent:5.2f}, {estimate:5.2f}, {abs(error):5.2f}, {error:5.2f});"
            cursor.execute(sql)
            mydb.commit()

    if print_rows:
        print()
        print(f"total: {total_error_abs:6.2f}, {total_error:6.2f}")
        print(f"squared: {squared_error:6.2f}")
        print(f"max: {max_error:6.2f}")
    
    return "finished"


def calculate_best_estimate(ranges, sliders={}, current_best=math.inf, best_sliders=None, slider_index=0):
    slider_name = range_keys[slider_index]
    current_range = ranges[slider_name]
    last_slider = len(ranges) == slider_index+1
    for i, slider_value in enumerate(current_range):
        current_slider = sliders.copy()
        current_slider[slider_name] = slider_value

        # if slider_index == 0:
            # print()
            # print(f"{i}/{len(current_range)}   current_best: {current_best:.2f}")
        if slider_index == 1:
            # print(f"---{i}/{len(current_range)}")
            print("-", end="")

        if last_slider:
            message = calculate_error(current_slider, min_error=current_best)
            error = total_error_abs
            if message == "error_exceeded":
                continue
                print(f"{current_best:.2f} < {error:.2f}")
            elif error < current_best:
                current_best = error
                best_sliders = current_slider
        else:
            (current_best, best_sliders) = calculate_best_estimate(ranges, current_slider, current_best, best_sliders, slider_index+1)

    return (current_best, best_sliders)


def print_ranges(ranges):
    print()
    total = len(card_table)
    print(f"cards: {len(card_table)}")
    for slider_name in ranges:
        slider_value = ranges[slider_name]
        total *= len(slider_value)
        print(f"{slider_name}: {len(slider_value)}")
    print(f"total: {total:,}")
    # print(f"ETA: {total*0.0000358613/len(card_table)}")
    print()


def print_sliders(sliders, steps=None):
    print()
    for slider_name in sliders:
        slider_value = sliders[slider_name]
        slider_string = f'"{slider_name}"'
        value_string = f'np.float64({slider_value:.2f})'

        if steps is None:
            print(f"    {slider_string}: {value_string},")
        else:
            step_string = f'{steps[slider_name]}'
            print(f"    {slider_string}: ({value_string}, {step_string}),")
        
    print()


def check_neighbors(slider_steps, save=False):
    ranges = {}
    best_sliders = {}
    steps = {}

    for name in range_keys:
        slider, step = slider_steps[name]
        best_sliders[name] = slider
        steps[name] = step

    calculate_error(best_sliders)
    current_best = total_error_abs

    for neighbors_checked in range(50):
        for i, name in enumerate(range_keys):
            start = best_sliders[name]
            offset = steps[name]
            if offset == 0:
                ranges[name] = [start]
            else:
                ranges[name] = [start-offset, start, start+offset]

        print(f"{neighbors_checked}: ", end="")
        error, current_slider  = calculate_best_estimate(ranges, current_best=current_best)
        print(f" {current_best:.2f} - {error:.2f}")
        if error >= current_best:
            break
        else:
            current_best = error
            best_sliders = current_slider
    else:
        print("LIMIT EXCEEDED")

    # print_sliders(best_sliders)
    print_sliders(best_sliders, steps)

    if save:
        calculate_error(best_sliders, save=save)


# check_neighbors(
#     slider_steps,
#     save=True
# )


sliders = {
    "card_adder": np.float64(2.00),
    "percent_adder": np.float64(22.00),
    "pair_adder": np.float64(27.00),
    "pair_scaler": np.float64(1.50),
    "high_card_scaler": np.float64(1.00),
    "low_card_scaler": np.float64(0.00),
    "connection_scaler": np.float64(0.00),
    "suited_adder": np.float64(2.50),
    "adjacent_adder_4": np.float64(2.50),
    "adjacent_adder_3": np.float64(2.00),
    "adjacent_adder_2": np.float64(1.00),
    "adjacent_adder_1": np.float64(0.50),
    "ace_adder": np.float64(1.50),
    "king_adder": np.float64(1.00),
    "queen_adder": np.float64(0.50),
    "jack_adder": np.float64(0.00),
    "10_adder": np.float64(0.00),
}

print(estimate_hand(12, 9, 'u', 2, sliders))

# calculate_error({
#     "percent_adder": np.float64(23.00),
#     "high_card_adder": np.float64(9.00),
#     "rank_multiplier": np.float64(0.10),
#     "ace_adder": np.float64(8.00),
#     "king_adder": np.float64(6.00),
#     "queen_adder": np.float64(5.00),
#     "jack_adder": np.float64(3.00),
#     "10_adder": np.float64(2.00),
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
