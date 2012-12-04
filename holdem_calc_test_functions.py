import random
from holdem_functions import *


# Helper function for main2
def parse_cards_test():
    cards, board = [], []
    cards.append((Card(sys.argv[1]), Card(sys.argv[2])))
    for arg in sys.argv[3:]:
        board.append(Card(arg))
    cards.append(board)
    return cards


# Testing function where you can specify one set of hole cards and board
# and will print out what hand we detect given these cards
def main2():
    hole_cards, flat_board = parse_cards_test()
    print detect_hand(hole_cards, flat_board)


# Test function where you can specify one set of hole cards and will generate
# num_iterations of boards and prints what hand we detect given these cards
def main3():
    hole_cards = parse_cards()
    deck = generate_deck(hole_cards)
    num_iterations = 10000
    for i in xrange(num_iterations):
        board = random.sample(deck, 5)
        for index, hole_card in enumerate(hole_cards):
            print hole_card
            print board
            print detect_hand(hole_card, board)
        print
