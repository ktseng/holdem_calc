import argparse
import re
import holdem_functions


def parse_args():
    # Define possible command line arguments
    parser = argparse.ArgumentParser(
        description="Find the odds that a Texas Hold'em hand will win. Note "
        "that cards must be given in the following format: As, Jc, Td, 3h.")
    parser.add_argument("cards", type=str, nargs="*", metavar="hole card",
        help="Hole cards you want to find the odds for.")
    parser.add_argument("-b", "--board", nargs="*", type=str, metavar="card",
        help="Add board cards")
    parser.add_argument("-e", "--exact", action="store_true",
        help="Find exact odds by enumerating every possible board")
    parser.add_argument("-n", type=int, default=100000,
        help="Run N Monte Carlo simulations")
    # Parse command line arguments and check for errors
    args = parser.parse_args()
    error_check(args)
    # Parse hole cards
    hole_cards = parse_hole_cards(args.cards)
    board = None
    # Create the deck. If the user has defined a board, parse the board.
    if args.board:
        board = parse_cards(args.board)
        all_cards = list(hole_cards)
        all_cards.append(board)
        deck = holdem_functions.generate_deck(all_cards)
    else:
        deck = holdem_functions.generate_deck(hole_cards)
    return hole_cards, args.n, args.exact, board, deck


# Error checking the command line arguments
def error_check(args):
    # Checking that the number of Monte Carlo simulations is a positive number
    if args.n <= 0:
        print "Number of Monte Carlo simulations must be positive."
        exit()
    # Checking that there are an even number of hole cards
    if len(args.cards) <= 0 or len(args.cards) % 2:
        print args.cards
        print "You must provide a non-zero even number of hole cards"
        exit()
    all_cards = list(args.cards)
    # Checking that the board length is either 3 or 4 (flop or flop + turn)
    if args.board:
        if len(args.board) != 3 and len(args.board) != 4:
            print "Board must have a length of 3 or 4."
            exit()
        all_cards.extend(args.board)
    # Checking that the hole cards + board are formatted properly and unique
    card_re = re.compile('[AKQJT98765432][scdh]')
    for card in all_cards:
        if not card_re.match(card):
            print "Invalid card given."
            exit()
        else:
            if all_cards.count(card) != 1:
                print "The cards given must be unique."
                exit()


# Returns tuple of two-tuple hole_cards: e.g. ((As, Ks), (Ad, Kd), (Jh, Th))
def parse_hole_cards(hole_cards):
    cards = parse_cards(hole_cards)
    # Create two-tuples out of hole cards
    hole_cards, current_hole_cards = [], []
    for hole_card in cards:
        current_hole_cards.append(hole_card)
        if len(current_hole_cards) == 2:
            hole_cards.append((current_hole_cards[0], current_hole_cards[1]))
            current_hole_cards = []
    return tuple(hole_cards)


# Instantiates new cards from the arguments and returns them in a tuple
def parse_cards(card_strings):
    return [holdem_functions.Card(arg) for arg in card_strings]
