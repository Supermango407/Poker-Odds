from webbrowser import get


cards = []
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'H', 'S']
rank_values = {rank: index for index, rank in enumerate(ranks)}

for rank in ranks:
    for suit in suits:
        cards.append((rank, suit))


def get_multiples(hand):
    """returns pairs three of a kind and four of a kind in a hand"""
    pairs = []
    three_of_a_kind = []
    four_of_a_kind = []

    rank_dict = {}
    for card in hand:
        rank = card[0]
        if rank in rank_dict:
            rank_dict[rank].append(card)
        else:
            rank_dict[rank] = [card]

    for rank, cards in rank_dict.items():
        if len(cards) == 2:
            pairs.append(cards)
        elif len(cards) == 3:
            three_of_a_kind.append(cards)
        elif len(cards) == 4:
            four_of_a_kind.append(cards)

    return {
        2: pairs,
        3: three_of_a_kind,
        4: four_of_a_kind
    }


def get_flush(hand):
    """returns all cards of the same suit in a hand if there is a flush,
     otherwise returns empty list"""
    
    suit_count = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
    for card in hand:
        suit = card[1]
        suit_count[suit] += 1
        if suit_count[suit] == 5:
            return [c for c in hand if c[1] == suit]

    return []


def get_straight(hand):
    """returns the highest rank in a straight if there is a straight, otherwise returns None."""
    sorted_ranks = sorted((rank_values[card[0]] for card in hand), reverse=True)
    sorted_ranks = list(dict.fromkeys(sorted_ranks))

    # Check for regular straights
    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i] - sorted_ranks[i + 4] == 4:
            return ranks[sorted_ranks[i]]
        
    # Check for the special case of A-2-3-4-5 straight
    if sorted_ranks[0] == 12 and sorted_ranks[-4:] == [3, 2, 1, 0]:
        return ranks[3] # return 5 as the highest card in the straight (A-2-3-4-5)


    return None


def get_best_hand(hands:list):
    """returns index of the best hand from a list of hands"""
    flushes = [get_flush(hand) for hand in hands]
    straights = [get_straight(hand) for hand in hands]


hands = [
    ["5S", "KC", "5C", "KD", "TC", "QS", "2S"], # 0
    ["3S", "9S", "2C", "AS", "KS", "KC", "5S"], # 1
    ["TS", "6C", "7C", "TC", "9H", "KC", "8C"], # 2
    ["JH", "9H", "8H", "QH", "TH", "QS", "4D"], # 3
    ["JS", "TS", "5C", "7H", "JD", "5S", "TC"], # 4
    ["8H", "4S", "6S", "8H", "6H", "8C", "5S"], # 5
    ["JD", "AD", "2D", "TD", "QD", "KD", "TS"], # 6
    ["TS", "2H", "3C", "TC", "5C", "TH", "KH"], # 7
    ["7H", "QD", "7D", "AC", "7S", "9H", "7C"], # 8
    ["3D", "6D", "4D", "QH", "QD", "7D", "5D"], # 9
    ["3S", "TS", "5S", "AS", "JS", "8S", "7S"], # 10
    ["AC", "4D", "3S", "2S", "AD", "TS", "5S"], # 11
    ["3D", "AC", "5C", "6S", "7D", "2S", "4S"] ,# 12
    ["3D", "AC", "5C", "6S", "7D", "2S", "4S"] ,# 13
    ["AS", "KD", "3C", "5C", "2C", "3D", "4C"] ,# 14
]

for i, hand in enumerate(hands):
    print(f"Hand {i}: {get_straight(hand)}")

# print(get_best_hand([hands[0], hands[1]]))

# def return_winner(hole1, hole2, board):
#     """calculates the winner between two hands given their hole cards and the board cards"""
