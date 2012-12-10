# Constants
suit_index_dict = {"s": 0, "c": 1, "h": 2, "d": 3}
reverse_suit_index = ("s", "c", "h", "d")
val_string = "AKQJT98765432"
hand_rankings = ("High Card", "Pair", "Two Pair", "Three of a Kind",
                 "Straight", "Flush", "Full House", "Four of a Kind",
                 "Straight Flush", "Royal Flush")
suit_value_dict = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
for num in xrange(2, 10):
    suit_value_dict[str(num)] = num


class Card:
    # Takes in strings of the format: "As", "Tc", "6d"
    def __init__(self, card_string):
        value, self.suit = card_string[0], card_string[1]
        self.value = suit_value_dict[value]
        self.suit_index = suit_index_dict[self.suit]

    def __str__(self):
        return val_string[14 - self.value] + self.suit

    def __repr__(self):
        return val_string[14 - self.value] + self.suit

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit


# Returns deck of cards with all hole cards removed
def generate_deck(taken_cards):
    deck = []
    for suit in reverse_suit_index:
        for ch in val_string:
            deck.append(Card(ch + suit))
    for taken_card in taken_cards:
        for card in taken_card:
            deck.remove(card)
    return tuple(deck)


# Generate num_iterations random boards
def generate_random_boards(deck, num_iterations, board_length):
    import random
    import time
    random.seed(time.time())
    for iteration in xrange(num_iterations):
        yield random.sample(deck, 5 - board_length)


# Generate all possible boards
def generate_exhaustive_boards(deck, num_iterations, board_length):
    import itertools
    return itertools.combinations(deck, 5 - board_length)


# Returns a board of cards all with suit = flush_index
def generate_suit_board(flat_board, flush_index):
    histogram = [card.value for card in flat_board
                                if card.suit_index == flush_index]
    histogram.sort(reverse=True)
    return histogram


# Returns a list of two tuples of the form: (value of card, frequency of card)
def preprocess(histogram):
    return [(14 - index, frequency) for index, frequency in
                                        enumerate(histogram) if frequency]


# Takes an iterable sequence and returns two items in a tuple:
# 1: 4-long list showing how often each card suit appears in the sequence
# 2: 13-long list showing how often each card value appears in the sequence
def preprocess_board(flat_board):
    suit_histogram, histogram = [0] * 4, [0] * 13
    # Reversing the order in histogram so in the future, we can traverse
    # starting from index 0
    for card in flat_board:
        histogram[14 - card.value] += 1
        suit_histogram[card.suit_index] += 1
    return suit_histogram, histogram, max(suit_histogram)


# Returns tuple: (Is there a straight flush?, high card)
def detect_straight_flush(suit_board):
    contiguous_length, fail_index = 1, len(suit_board) - 5
    # Won't overflow list because we fail fast and check ahead
    for index, elem in enumerate(suit_board):
        current_val, next_val = elem, suit_board[index + 1]
        if next_val == current_val - 1:
            contiguous_length += 1
            if contiguous_length == 5:
                return True, current_val + 3
        else:
            # Fail fast if straight not possible
            if index >= fail_index:
                if (index == fail_index and next_val == 5 and
                                                    suit_board[0] == 14):
                    return True, 5
                break
            contiguous_length = 1
    return False,


# Returns the highest kicker available
def detect_highest_quad_kicker(histogram_board):
    for elem in histogram_board:
        if elem[1] < 4:
            return elem[0]


# Returns tuple: (Is there a straight?, high card)
def detect_straight(histogram_board):
    contiguous_length, fail_index = 1, len(histogram_board) - 5
    # Won't overflow list because we fail fast and check ahead
    for index, elem in enumerate(histogram_board):
        current_val, next_val = elem[0], histogram_board[index + 1][0]
        if next_val == current_val - 1:
            contiguous_length += 1
            if contiguous_length == 5:
                return True, current_val + 3
        else:
            # Fail fast if straight not possible
            if index >= fail_index:
                if (index == fail_index and next_val == 5 and
                                        histogram_board[0][0] == 14):
                    return True, 5
                break
            contiguous_length = 1
    return False,


# Returns tuple of the two highest kickers that result from the three of a kind
def detect_three_of_a_kind_kickers(histogram_board):
    kicker1 = -1
    for elem in histogram_board:
        if elem[1] != 3:
            if kicker1 == -1:
                kicker1 = elem[0]
            else:
                return kicker1, elem[0]


# Returns the highest kicker available
def detect_highest_kicker(histogram_board):
    for elem in histogram_board:
        if elem[1] == 1:
            return elem[0]


# Returns tuple: (kicker1, kicker2, kicker3)
def detect_pair_kickers(histogram_board):
    kicker1, kicker2 = -1, -1
    for elem in histogram_board:
        if elem[1] != 2:
            if kicker1 == -1:
                kicker1 = elem[0]
            elif kicker2 == -1:
                kicker2 = elem[0]
            else:
                return kicker1, kicker2, elem[0]


# Returns a list of the five highest cards in the given board
# Note: Requires a sorted board to be given as an argument
def get_high_cards(histogram_board):
    return histogram_board[:5]


# Return Values:
# Royal Flush: (9,)
# Straight Flush: (8, high card)
# Four of a Kind: (7, quad card, kicker)
# Full House: (6, trips card, pair card)
# Flush: (5, [flush high card, flush second high card, ..., flush low card])
# Straight: (4, high card)
# Three of a Kind: (3, trips card, (kicker high card, kicker low card))
# Two Pair: (2, high pair card, low pair card, kicker)
# Pair: (1, pair card, (kicker high card, kicker med card, kicker low card))
# High Card: (0, [high card, second high card, third high card, etc.])
def detect_hand(hole_cards, given_board, suit_histogram,
                                            full_histogram, max_suit):
    # Determine if flush possible. If yes, four of a kind and full house are
    # impossible, so return royal, straight, or regular flush.
    if max_suit >= 3:
        flush_index = suit_histogram.index(max_suit)
        for hole_card in hole_cards:
            if hole_card.suit_index == flush_index:
                max_suit += 1
        if max_suit >= 5:
            flat_board = list(given_board)
            flat_board.extend(hole_cards)
            suit_board = generate_suit_board(flat_board, flush_index)
            result = detect_straight_flush(suit_board)
            if result[0]:
                return (8, result[1]) if result[1] != 14 else (9,)
            return 5, get_high_cards(suit_board)

    # Add hole cards to histogram data structure and process it
    full_histogram = full_histogram[:]
    for hole_card in hole_cards:
        full_histogram[14 - hole_card.value] += 1
    histogram_board = preprocess(full_histogram)

    # Find which card value shows up the most and second most times
    current_max, max_val, second_max, second_max_val = 0, 0, 0, 0
    for item in histogram_board:
        val, frequency = item[0], item[1]
        if frequency > current_max:
            second_max, second_max_val = current_max, max_val
            current_max, max_val = frequency, val
        elif frequency > second_max:
            second_max, second_max_val = frequency, val

    # Check to see if there is a four of a kind
    if current_max == 4:
        return 7, max_val, detect_highest_quad_kicker(histogram_board)
    # Check to see if there is a full house
    if current_max == 3 and second_max >= 2:
        return 6, max_val, second_max_val
    # Check to see if there is a straight
    if len(histogram_board) >= 5:
        result = detect_straight(histogram_board)
        if result[0]:
            return 4, result[1]
    # Check to see if there is a three of a kind
    if current_max == 3:
        return 3, max_val, detect_three_of_a_kind_kickers(histogram_board)
    if current_max == 2:
        # Check to see if there is a two pair
        if second_max == 2:
            return 2, max_val, second_max_val, detect_highest_kicker(
                                                            histogram_board)
        # Return pair
        else:
            return 1, max_val, detect_pair_kickers(histogram_board)
    # Check for high cards
    return 0, get_high_cards(histogram_board)


# Returns the index of the player with the winning hand
def compare_hands(result_list):
    best_hand = max(result_list)
    winning_player_index = result_list.index(best_hand) + 1
    # Check for ties
    if best_hand in result_list[winning_player_index:]:
        return 0
    return winning_player_index


# Print results
def print_results(hole_cards, winner_list, result_histograms):
    float_iterations = float(sum(winner_list))
    print "Winning Percentages:"
    for index, hole_card in enumerate(hole_cards):
        print hole_card, ": ", float(winner_list[index + 1]) / float_iterations
    print "Ties: ", float(winner_list[0]) / float_iterations, "\n"
    for player_index, histogram in enumerate(result_histograms):
        print "Player" + str(player_index + 1) + " Histogram: "
        for index, elem in enumerate(histogram):
            print hand_rankings[index], ": ", float(elem) / float_iterations
        print
