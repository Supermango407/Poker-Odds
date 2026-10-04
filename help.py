cards = []
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'H', 'S']
rank_values = {rank: index for index, rank in enumerate(ranks)}

for rank in ranks:
    for suit in suits:
        cards.append(rank+suit)


def get_multiples(hand, is_sorted=False):
    """returns pairs three of a kind and four of a kind in a hand"""
    if not is_sorted:
        hand = sorted(hand, key=lambda card: rank_values[card[0]], reverse=True)
        
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


def get_flush(hand, is_sorted=False):
    """returns all cards of the same suit in a hand if there is a flush,
     otherwise returns empty list"""
    if not is_sorted:
        hand = sorted(hand, key=lambda card: rank_values[card[0]], reverse=True)

    suit_count = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
    for card in hand:
        suit = card[1]
        suit_count[suit] += 1
        if suit_count[suit] == 5:
            return [c for c in hand if c[1] == suit]

    return []


def get_straight(hand, is_sorted=False):
    """returns the highest rank in a straight if there is a straight, otherwise returns None."""
    if not is_sorted:
        hand = sorted(hand, key=lambda card: rank_values[card[0]], reverse=True)

    sorted_ranks = [rank_values[card[0]] for card in hand]
    sorted_ranks = list(dict.fromkeys(sorted_ranks)) # remove duplicates while preserving order

    # Check for regular straights
    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i] - sorted_ranks[i + 4] == 4:
            return ranks[sorted_ranks[i]]
        
    # Check for the special case of A-2-3-4-5 straight
    if sorted_ranks[0] == 12 and sorted_ranks[-4:] == [3, 2, 1, 0]:
        return ranks[3] # return 5 as the highest card in the straight (A-2-3-4-5)


    return None


def get_best_hand(hands:list, print_hands=False):
    """returns indices of the best hands from a list of hands"""
    # sort hands by rank values
    for i in range(len(hands)):
        hands[i] = sorted(hands[i], key=lambda card: rank_values[card[0]], reverse=True)

    straights = [get_straight(hand, is_sorted=True) for hand in hands]
    flushes = [get_flush(hand, is_sorted=True) for hand in hands]

    pairs = []
    trips = []
    fours = []
    for hand in hands:
        multiples = get_multiples(hand)
        pairs.append(multiples[2])
        trips.append(multiples[3])
        fours.append(multiples[4])
        # print(f"2: {multiples[2]}")
        # print(f"3: {multiples[3]}")
        # print(f"4: {multiples[4]}")
        # print()

    top_hands = []
    current_highest =  None

    # check for straight flushes
    for i, flush in enumerate(flushes):
        if flush:
            straight_flush = get_straight(flush)
            if straight_flush:
                if current_highest is None or rank_values[straight_flush] > current_highest:
                    top_hands = [i]
                    current_highest = rank_values[straight_flush][:5]
                elif rank_values[straight_flush] == current_highest:
                    top_hands.append(i)

    if top_hands:
        if print_hands:
            print("Straight Flushes:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for four of a kinds
    for i, four in enumerate(fours):
        if four:
            four_rank = four[0][0][0]
            if current_highest is None or rank_values[four_rank] > current_highest:
                top_hands = [i]
                current_highest = rank_values[four_rank]
            elif rank_values[four_rank] == current_highest:
                top_hands.append(i)

    if top_hands:
        if print_hands:
            print("Four of a Kinds:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for full houses
    for i in range(len(hands)):
        if trips[i] and pairs[i]:
            trip_rank = trips[i][0][0][0]
            pair_rank = pairs[i][0][0][0]
            if current_highest is None or (rank_values[trip_rank], rank_values[pair_rank]) > current_highest:
                top_hands = [i]
                current_highest = (rank_values[trip_rank], rank_values[pair_rank])
            elif (rank_values[trip_rank], rank_values[pair_rank]) == current_highest:
                top_hands.append(i)

    if top_hands:
        if print_hands:
            print("Full Houses:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for flushes
    for i, flush in enumerate(flushes):
        if flush:
            flush_ranks = [rank_values[card[0]] for card in flush]
            if current_highest is None or flush_ranks > current_highest:
                top_hands = [i]
                current_highest = flush_ranks[:5]
            elif flush_ranks == current_highest:
                top_hands.append(i)

    if top_hands:
        if print_hands:
            print("Flushes:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands
    

    # check for straights
    for i, straight in enumerate(straights):
        if straight:
            straight_rank = rank_values[straight][:5]
            if current_highest is None or straight_rank > current_highest:
                top_hands = [i]
                current_highest = straight_rank
            elif straight_rank == current_highest:
                top_hands.append(i)

    if top_hands:
        if print_hands:
            print("Straights:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for three of a kinds
    for i, trip in enumerate(trips):
        if trip:
            trip_rank = trip[0][0][0]
            if current_highest is None or rank_values[trip_rank] > current_highest:
                top_hands = [i]
                current_highest = rank_values[trip_rank]
            elif rank_values[trip_rank] == current_highest:
                top_hands.append(i)
                
    if top_hands:
        if print_hands:
            print("Three of a Kinds:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for two pairs
    for i, pair in enumerate(pairs):
        if len(pair) >= 2:
            pair_ranks = [rank_values[p[0][0]] for p in pair][:2]
            if current_highest is None or pair_ranks > current_highest:
                top_hands = [i]
                current_highest = pair_ranks
            elif pair_ranks == current_highest:
                top_hands.append(i)
                
    if top_hands:
        if print_hands:
            print("Two Pairs:")
            for i in top_hands:
                print(f"|--- Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for pairs
    for i, pair in enumerate(pairs):
        if pair:
            pair_rank = pair[0][0][0]
            if current_highest is None or rank_values[pair_rank] > current_highest:
                top_hands = [i]
                current_highest = rank_values[pair_rank]
            elif rank_values[pair_rank] == current_highest:
                top_hands.append(i)
                
    if top_hands:
        if print_hands:
            print("Pairs:")
            for i in top_hands:
                print(f"|---Hand {i}: {hands[i]}")
            print()
        return top_hands


    # check for high card
    for i, hand in enumerate(hands):
        hand_ranks = [rank_values[card[0]] for card in hand][:5]
        if current_highest is None or hand_ranks > current_highest:
            top_hands = [i]
            current_highest = hand_ranks
        elif hand_ranks == current_highest:
            top_hands.append(i)
    
    if print_hands:
        print("High Cards:")
        for i in top_hands:
            print(f"|---Hand {i}: {hands[i]}")
        print()

    return top_hands


def get_winners(holes, board, print_hands=False):
    """returns indices of the winning hands from a list of hole cards and a board"""
    hands = [hole + board for hole in holes]
    return get_best_hand(hands, print_hands)


# hands = [
#     ["5S", "KC", "5C", "KD", "TC", "QS", "2S"], # 0
#     ["3S", "9S", "2C", "AS", "KS", "KC", "5S"], # 1
#     ["TS", "6C", "7C", "TC", "9H", "KC", "8C"], # 2
#     ["7D", "3C", "4D", "5D", "6D", "8D", "9C"], # 3
#     ["JH", "9H", "8H", "QH", "TH", "QS", "4D"], # 4
#     ["JS", "TS", "5C", "7H", "JD", "5S", "TC"], # 5
#     ["8H", "4S", "6S", "8H", "6H", "8C", "5S"], # 6
#     ["JD", "AD", "2D", "TD", "QD", "KD", "TS"], # 7
#     ["TS", "2H", "3C", "TC", "5C", "TH", "KH"], # 8
#     ["7H", "QD", "7D", "AC", "7S", "9H", "7C"], # 9
#     ["3D", "6D", "4D", "QH", "QD", "7D", "5D"], # 10
#     ["3S", "TS", "5S", "AS", "JS", "8S", "7S"], # 11
#     ["AC", "4D", "3S", "2S", "AD", "TS", "5S"], # 12
#     ["3D", "AC", "5C", "6S", "7D", "2S", "4S"], # 13
#     ["3D", "AC", "5C", "6S", "7D", "2S", "4S"], # 14
#     ["AS", "KD", "3C", "5C", "2C", "3D", "4C"], # 15
#     ["6H", "3C", "TH", "5C", "2C", "4C", "AC"], # 16
#     ["AH", "TH", "QH", "JH", "AD", "KH", "AD"], # 17
#     ["TS", "JS", "9C", "AH", "AS", "TH", "AC"], # 18
#     ["TC", "AD", "AS", "JD", "8S", "TD", "TC"], # 19
#     ["5H", "KD", "8C", "5C", "8D", "KH", "7D"], # 20
#     ["AD", "QD", "8C", "3S", "5C", "4D", "6C"], # 21
#     ["AD", "QD", "8C", "2S", "5C", "3D", "6C"], # 22
# ]

# print(get_best_hand(hands))

# holes = [
#     ["9S", "9C"], # 0
#     ["9D", "9H"], # 1
# ]

# board = ["5C", "KD", "TC", "QS", "2S"]

# get_winners(holes, board, True)

