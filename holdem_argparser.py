import argparse
import re
import holdem_functions


# Wrapper class which holds the arguments for library calls
# Mocks actual argparse object
class LibArgs:
    def __init__(self, board, exact, num, input_file, hole_cards):
        self.board = board
        self.cards = hole_cards
        self.n = num
        self.input = input_file
        self.exact = exact

# Parses arguments passed to holdem_calc as a library call
def parse_lib_args(args):
    error_check_arguments(args)
    # Parse hole cards and board
    hole_cards, board = None, None
    if not args.input:
        hole_cards, board = parse_cards(args.cards, args.board)
    return hole_cards, args.n, args.exact, board, args.input

# Parses command line arguments to holdem_calc
def parse_args():
    # Define possible command line arguments
    parser = argparse.ArgumentParser(
        description="Find the odds that a Texas Hold'em hand will win. Note "
        "that cards must be given in the following format: As, Jc, Td, 3h.")
    parser.add_argument("cards", nargs="*", type=str, metavar="hole card",
                        help="Hole cards you want to find the odds for.")
    parser.add_argument("-b", "--board", nargs="*", type=str, metavar="card",
                        help="Add board cards")
    parser.add_argument("-e", "--exact", action="store_true",
                        help="Find exact odds by enumerating every possible "
                        "board")
    parser.add_argument("-n", type=int, default=100000,
                        help="Run N Monte Carlo simulations")
    parser.add_argument("-i", "--input", type=str,
                        help="Read hole cards and boards from an input file. "
                        "Commandline arguments for hole cards and board will "
                        "be ignored")
    # Parse command line arguments and check for errors
    args = parser.parse_args()
    error_check_arguments(args)
    # Parse hole cards and board
    hole_cards, board = None, None
    if not args.input:
        hole_cards, board = parse_cards(args.cards, args.board)
    return hole_cards, args.n, args.exact, board, args.input

# Parses a line taken from the input file and returns the hole cards and board
def parse_file_args(line):
    if line is None or len(line) == 0:
        print(line)
        print("Invalid format")
        exit()
    values = line.split("|")
    if len(values) > 2 or len(values) < 1:
        print(line)
        print("Invalid format")
        exit()
    hole_cards = values[0].split()
    all_cards = list(hole_cards)
    board = None
    if len(values) == 2:
        board = values[1].split()
        all_cards.extend(board)
    error_check_cards(all_cards)
    return parse_cards(hole_cards, board)

# Parses hole cards and board
def parse_cards(cards, board):
    hole_cards = create_hole_cards(cards)
    if board:
        board = parse_board(board)
    return hole_cards, board

# Error check the command line arguments
def error_check_arguments(args):
    # Check that the number of Monte Carlo simulations is a positive number
    if args.n <= 0:
        print("Number of Monte Carlo simulations must be positive.")
        exit()
    # Check that we can open the specified input file
    if args.input:
        file_name = args.input
        try:
            input_file = open(file_name, 'r')
            input_file.close()
        except IOError:
            print("Error opening file " + file_name)
            exit()
    # Check to make sure all cards are of a valid format
    all_cards = list(args.cards)
    if args.board:
        all_cards.extend(args.board)
    error_check_cards(all_cards)

# Error check the command line arguments
def error_check_arguments(args):
    # Check that the number of Monte Carlo simulations is a positive number
    if args.n <= 0:
        print("Number of Monte Carlo simulations must be positive.")
        exit()
    # Check that we can open the specified input file
    if args.input:
        file_name = args.input
        try:
            input_file = open(file_name, 'r')
            input_file.close()
        except IOError:
            print("Error opening file " + file_name)
            exit()
    # Check to make sure all cards are of a valid format
    all_cards = list(args.cards)
    if args.board:
        all_cards.extend(args.board)
    error_check_cards(all_cards)

# Checking that the hole cards + board are formatted properly and unique
def error_check_cards(all_cards):
    card_re = re.compile('[AKQJT98765432][scdh]')
    for card in all_cards:
        if card != "?" and not card_re.match(card):
            print("Invalid card given.")
            exit()
        else:
            if all_cards.count(card) != 1 and card != "?":
                print("The cards given must be unique.")
                exit()

# Returns tuple of two-tuple hole_cards: e.g. ((As, Ks), (Ad, Kd), (Jh, Th))
def create_hole_cards(raw_hole_cards):
    # Checking that there are an even number of hole cards
    if (raw_hole_cards is None or len(raw_hole_cards) < 2 or
            len(raw_hole_cards) % 2):
        print("You must provide a non-zero even number of hole cards")
        exit()
    # Create two-tuples out of hole cards
    hole_cards, current_hole_cards = [], []
    for hole_card in raw_hole_cards:
        if hole_card != "?":
            current_card = holdem_functions.Card(hole_card)
            current_hole_cards.append(current_card)
        else:
            current_hole_cards.append(None)
        if len(current_hole_cards) == 2:
            if None in current_hole_cards:
                if (current_hole_cards[0] is not None or
                        current_hole_cards[1] is not None):
                    print("Unknown hole cards must come in pairs")
                    exit()
            hole_cards.append((current_hole_cards[0], current_hole_cards[1]))
            current_hole_cards = []
    if hole_cards.count((None, None)) > 1:
        print("Can only have one set of unknown hole cards")
    return tuple(hole_cards)

# Returns list of board cards: e.g. [As Ks Ad Kd]
def parse_board(board):
    if len(board) > 5 or len(board) < 3:
        print("Board must have a length of 3, 4, or 5.")
        exit()
    if "?" in board:
        print("Board cannot have unknown cards")
        exit()
    return create_cards(board)

# Instantiates new cards from the arguments and returns them in a tuple
def create_cards(card_strings):
    return [holdem_functions.Card(arg) for arg in card_strings]
