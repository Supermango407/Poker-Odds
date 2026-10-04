import csv
import help

input_file = "hole_odds/hole_odds_2.csv"
output_file = "hole_odds/converted_2.csv"

card_offset = 13
percent_offset = 0
high_card_multiplier = 1.75
low_card_multiplier = 1.0
pair_multiplier = 1.333333333
suited_adder = 2
connection_adder = 0
connection_multiplier = 0

table = []

total_error = 0
total_error_abs = 0

unsuited_error = 0
unsuited_error_abs = 0

suited_error = 0
suited_error_abs = 0

paired_error = 0
paired_error_abs = 0



with open(input_file, mode='r', newline='') as file:
    reader = csv.reader(file)

    for i, input_row in enumerate(reader):
        hole_name = ""
        modifier = "" # s:suited, u:unsuited, p:pair.
        seperation = 0

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

        estimation = (high_card+card_offset)*high_card_multiplier
        estimation += (low_card+card_offset)*low_card_multiplier

        if modifier == 's':
            estimation += suited_adder
        elif modifier == 'p':
            estimation *= pair_multiplier

        estimation += (connected+connection_adder) * connection_multiplier

        estimation += percent_offset

        error = estimation-(win_percent+draw_percent)
        total_error += error
        total_error_abs += abs(error)

        if modifier == 'u':
            unsuited_error += error
            unsuited_error_abs += abs(error)
            # continue
        elif modifier == 's':
            suited_error += error
            suited_error_abs += abs(error)
            continue
        elif modifier == 'p':
            paired_error += error
            paired_error_abs += abs(error)
            continue
        else:
            print(f"error: {modifier}")

        table.append((hole_name, modifier, connected, f"{win_percent+draw_percent:5.2f}", f"{estimation:5.2f}", f"{error:5.2f}"))


print(f"total: {total_error_abs:6.2f}, {total_error:6.2f}")
print(f"unsuited: {unsuited_error_abs:6.2f}, {unsuited_error:6.2f}")
print(f"suited: {suited_error_abs:6.2f}, {suited_error:6.2f}")
print(f"paired: {paired_error_abs:6.2f}, {paired_error:6.2f}")

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(table)

