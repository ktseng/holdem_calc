import sys

# Global variables
suit_index_dict = {"s": 0, "c": 1, "h": 2, "d": 3}
reverse_suit_index = ("s", "c", "h", "d")
val_string = "23456789TJQKA"
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
        return val_string[self.value - 2] + self.suit

    def __repr__(self):
        return val_string[self.value - 2] + self.suit

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit


# Returns tuple of hole_cards: e.g. ((As, Ks), (Ad, Kd), (Jh, Th))
def parse_cards():
    # Iterate over command line arguments, convert them into cards, and append
    # them into the cards list
    cards = []
    for arg in sys.argv[1:]:
        new_card = Card(arg)
        cards.append(new_card)
    # Create two-tuples out of hole cards
    hole_cards = []
    current_hole_cards = []
    for hole_card in cards:
        current_hole_cards.append(hole_card)
        if len(current_hole_cards) == 2:
            hole_cards.append((current_hole_cards[0], current_hole_cards[1]))
            current_hole_cards = []
    return tuple(hole_cards)


# Returns deck of cards with all hole cards removed
def generate_deck(hole_cards):
    deck = []
    for suit in reverse_suit_index:
        for ch in val_string:
            deck.append(Card(ch + suit))
    for hole_card in hole_cards:
        for card in hole_card:
            deck.remove(card)
    return tuple(deck)


# Returns a board of cards all with suit = flush_index
def generate_suit_board(flat_board, flush_index):
    return [card for card in flat_board if card.suit_index == flush_index]


# Returns board in the following format: e.g. [2, 1, 1, 1] where:
# Index0 = Spades, Index1 = Clubs, Index2 = Hearts, Index4 = Diamonds
def generate_suit_histogram(flat_board):
    suit_histogram = [0] * 4
    for card in flat_board:
        suit_histogram[card.suit_index] += 1
    return suit_histogram


# Returns three items in a tuple:
# 1: Sorted list of two-tuples formatted: (card value, number of occurrences)
# 2: Two-tuple: (most number of times a card shows up, card value)
# 3: Two-tuple: (2nd most number of times a card shows up, card value)
def generate_histogram_board(flat_board):
    histogram, board = [0] * 13, []
    for card in flat_board:
        histogram[card.value - 2] += 1
    current_max, max_val, second_max, second_max_val = 0, 0, 0, 0
    for index, frequency in enumerate(histogram):
        if frequency != 0:
            val = index + 2
            board.append((val, frequency))
            if frequency >= current_max:
                second_max, second_max_val = current_max, max_val
                current_max, max_val = frequency, val
            elif frequency >= second_max:
                second_max, second_max_val = frequency, val
    return board, (current_max, max_val), (second_max, second_max_val)


# Returns tuple: (Is there a straight flush?, straight flush high card)
def detect_straight_flush(board):
    return detect_straight(generate_histogram_board(board)[0])


# Returns the highest kicker available
def detect_highest_quad_kicker(histogram_board):
    index = len(histogram_board) - 1
    while index >= 0:
        if histogram_board[index][1] < 4:
            return histogram_board[index][0]
        index -= 1


# Returns tuple: (Flush High card1, Flush High card2, Flush High card3, etc.)
def get_flush_high_cards(suit_board):
    suit_board.sort(key=lambda card: card.value)
    result = [card.value for card in suit_board[-5:]]
    result.reverse()
    return tuple(result)


# Returns tuple: (Is there a straight?, high card)
def detect_straight(histogram_board):
    index = len(histogram_board) - 1
    last_value = histogram_board[index][0]
    contiguous_length = 1
    while index >= 1:
        current_val = histogram_board[index][0]
        if histogram_board[index - 1][0] == current_val - 1:
            contiguous_length += 1
        else:
            contiguous_length = 1
        index -= 1
        if (index == 0 and last_value == 14 and
            contiguous_length == 4 and histogram_board[index][0] == 2):
            return True, 5
        if contiguous_length == 5:
            return True, current_val + 3
    return False,


# Returns tuple of the two highest kickers that result from the three of a kind
def detect_three_of_a_kind_kickers(histogram_board):
    index = len(histogram_board) - 1
    kicker1 = -1
    while index >= 0:
        if histogram_board[index][1] != 3:
            if kicker1 == -1:
                kicker1 = histogram_board[index][0]
            else:
                return kicker1, histogram_board[index][0]
        index -= 1


# Returns the highest kicker available
def detect_highest_kicker(histogram_board):
    index = len(histogram_board) - 1
    while index >= 0:
        if histogram_board[index][1] == 1:
            return histogram_board[index][0]
        index -= 1


# Returns tuple: (kicker1, kicker2, kicker3)
def detect_pair_kickers(histogram_board):
    # Iterate through the histogram board to see where two pair is
    index = len(histogram_board) - 1
    kicker1, kicker2 = -1, -1
    while index >= 0:
        if histogram_board[index][1] != 2:
            if kicker1 == -1:
                kicker1 = histogram_board[index][0]
            elif kicker2 == -1:
                kicker2 = histogram_board[index][0]
            else:
                return kicker1, kicker2, histogram_board[index][0]
        index -= 1


# Returns a tuple of the five highest cards in the given board
# Note: Requires a sorted board to be given as an argument
def get_high_cards(histogram_board):
    result = [elem[0] for elem in histogram_board[-5:]]
    result.reverse()
    return tuple(result)


# Return Values:
# Royal Flush: (9,)
# Straight Flush: (8, high card)
# Four of a Kind: (7, quad card, kicker)
# Full House: (6, trips card, pair card)
# Flush: (5, (flush high card, flush second high card, ..., flush low card))
# Straight: (4, high card)
# Three of a Kind: (3, trips card, (kicker high card, kicker low card))
# Two Pair: (2, high pair card, low pair card, kicker)
# Pair: (1, pair card, (kicker high card, kicker med card, kicker low card))
# High Card: (0, (high card, second high card, third high card, etc.))
def detect_hand(hole_cards, given_board):
    # Pre-processing
    flat_board = [card for card in given_board]
    for hole_card in hole_cards:
        flat_board.append(hole_card)
    suit_board = None
    suit_histogram = generate_suit_histogram(flat_board)
    histogram_board, maximum, next_max = generate_histogram_board(flat_board)
    current_max, max_val = maximum
    second_max, second_max_val = next_max

    ## Find out the highest possible poker hand given the board + hole cards
    # Determine if flush possible at the top to minimize future work
    result = None
    max_suit = max(suit_histogram)
    flush_possible = True if max_suit >= 5 else False
    # If flush is possible, check if there is a royal flush or straight flush
    if flush_possible:
        # Royal flush is just a straight flush to the Ace, so we can re-use the
        # detect_straight_flush() function
        flush_index = suit_histogram.index(max_suit)
        suit_board = generate_suit_board(flat_board, flush_index)
        result = detect_straight_flush(suit_board)
        if result[0]:
            return (9,) if result[1] == 14 else (8, result[1])
    # Check to see if there is a four of a kind
    if current_max == 4:
        return 7, max_val, detect_highest_quad_kicker(histogram_board)
    # Check to see if there is a full house
    if current_max == 3 and second_max >= 2:
        return 6, max_val, second_max_val
    # Check to see if there is a flush
    if flush_possible:
        return 5, get_flush_high_cards(suit_board)
    # Check to see if there is a straight
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
        # Check to see if there is a pair
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
