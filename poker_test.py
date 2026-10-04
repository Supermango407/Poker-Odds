import random
import help

seed = 0
players = 2

while True:
    rng = random.Random(seed)
    cards_clone = help.cards.copy()
    rng.shuffle(cards_clone)
    holes = []

    for i in range(players):
        holes.append([cards_clone.pop(), cards_clone.pop()])

    board = [cards_clone.pop() for _ in range(5)]
    

    print("-"*40)
    print(f"Seed: {seed}")
    print(f"board: {board}")
    print(f"holes:")
    for i in range(players):
        print(f"  {i}: {holes[i]}")

    text = input()
    help.get_winners(holes, board, True)
    print("-"*40)

    input("Press Enter to continue")
    if text == "q":
        break

    seed += 1
