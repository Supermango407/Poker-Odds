import mysql.connector
import help

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Poker"
)
cursor = mydb.cursor(buffered=True)

def fill_cards():
    # Fill the cards table with all 52 cards
    for card in help.cards:
        rank, suit = card
        cursor.execute(f"INSERT INTO `cards` (`id`, `rank`, `suit`) VALUES (NULL, '{rank}', '{suit}');")


def fill_holes():
    # Fill the holes table with all 1,326 possible hole card combinations (including suited and offsuit)

    for i in range(len(help.cards)):
        for j in range(i + 1, len(help.cards)):
            card1 = help.cards[i]
            card2 = help.cards[j]
            rank1, suit1 = card1
            rank2, suit2 = card2

            cursor.execute(f"INSERT INTO `holes` (`id`, `cards`) VALUES (NULL, '{rank1}{suit1},{rank2}{suit2}');")

fill_cards()
fill_holes()

mydb.commit()
