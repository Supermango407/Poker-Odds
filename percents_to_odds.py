import csv
outfile_name = "output.csv"

table = []

with open('poker_odds_test.csv', mode='r') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        table_row = []
        for j, column in enumerate(row):
            if j == 0:
                table_row.append(column)  # Keep the header column
                continue

            percent = float(column)
            if percent == 0:
                odds = 'Infinity'
            else:
                odds = (100 / percent) - 1
            # print(f"Percent: {percent}%, Odds: {odds}")
            table_row.append(f"{odds:7.2f}")  # Format odds to 2 decimal places
        table.append(table_row)

# write the output to a new CSV file
with open(outfile_name, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(table)
