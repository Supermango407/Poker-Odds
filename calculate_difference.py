import help
import math
import numpy as np
import mysql.connector
from dataclasses import dataclass

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)
cursor = mydb.cursor(buffered=True)

sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 'u' ORDER BY `lose` DESC;"
cursor.execute(sql)
unsuited_hands = cursor.fetchall()

sql = "SELECT * FROM `2_player_holes` WHERE `modifier` LIKE 's' ORDER BY `lose` DESC;"
cursor.execute(sql)
suited_hands = cursor.fetchall()

total_error = 0.0
total_error_abs = 0.0
total_error_sqr = 0.0
total_error_max = 0.0


@dataclass
class SliderInputs():
    suited_adder: 0.0
    suited_multiplier: 1.0


def estimate_suited(unsuited, sliders:SliderInputs):
    high_suit_offset = 0.0
    if unsuited > 55:
        high_suit_offset = -0.5
    elif unsuited < 45:
        high_suit_offset = 0.5
    # high_suit_offset = 0.0
    
    return unsuited + sliders.suited_adder + high_suit_offset


def calculate_error(sliders:SliderInputs):
    global total_error, total_error_abs, total_error_sqr, total_error_max

    total_error = 0.0
    total_error_abs = 0.0
    total_error_sqr = 0.0
    total_error_max = 0.0

    for i in range(len(unsuited_hands)):
        name = unsuited_hands[i][1]
        unsuited_odds = unsuited_hands[i][6]+unsuited_hands[i][8]
        suited_odds = suited_hands[i][6]+suited_hands[i][8]
        difference = suited_odds - unsuited_odds
        
        estimate = estimate_suited(unsuited_odds, sliders)

        error = suited_odds-estimate

        total_error += error
        total_error_abs += abs(error)
        total_error_sqr += error**2
        total_error_max = max(total_error_max, error)

        print(f"{name}: {unsuited_odds:5.2f}  {suited_odds:5.2f}  {estimate:5.2f}  {error:5.2f}")


# adder_ranges = np.arange(0, 5, 0.1)
# multiplier_ranges = np.arange(0.0, 1.0, 1)

# current_best = math.inf
# best_sliders = None
# for i, adder in enumerate(adder_ranges):
#     print(f"{i}/{len(adder_ranges)}")
#     for multiplier in multiplier_ranges:
#         current_sliders = SliderInputs(adder, multiplier)
#         calculate_error(current_sliders)
#         current_error = total_error_sqr
#         if current_error < current_best:
#             current_best = current_error
#             best_sliders = current_sliders


# print(f"{best_sliders.suited_adder:5.2}, {best_sliders.suited_multiplier:5.2}")
# print(current_best)

calculate_error(SliderInputs(2.6, 0.0))
print(total_error_sqr)
