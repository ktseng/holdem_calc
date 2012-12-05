import time
import itertools
import holdem_functions

deck = None
num_iterations = 100000


# Generating boards
def generate_random_boards():
    import random
    random.seed(time.time())
    for iteration in xrange(num_iterations):
        yield random.sample(deck, 5)


# Generate all possible boards
def generate_exhaustive_boards():
    return itertools.combinations(deck, 5)


# Driver function which parses the command line arguments into hole cards,
# instantiates data structures to hold the intermediate results of the
# simulations, performs num_iterations simulations, and prints the results
def main():
    global deck
    # Parse command line arguments into hole cards and create deck
    hole_cards = holdem_functions.parse_cards()
    deck = holdem_functions.generate_deck(hole_cards)
    # Create results data structures which tracks results of comparisons
    # 1) result_histograms: a list for each player that shows the number of
    #    times each type of poker hand (e.g. flush, straight) was gotten
    # 2) winner_list: number of times each player wins the given round
    # 3) result_list: list of the best possible poker hand for each pair of
    #    hole cards for a given board
    num_players = len(hole_cards)
    result_list, winner_list = [None] * num_players, [0] * (num_players + 1)
    result_histograms = []
    for player in xrange(num_players):
        result_histograms.append([0] * 10)
    # Run num_iterations simulations
    generate_boards = generate_random_boards
    for board in generate_boards():
        # Find the best possible poker hand given the created board and the
        # hole cards and save them in the results data structures
        suit_histogram, histogram = holdem_functions.preprocess_board(board)
        for index, hole_card in enumerate(hole_cards):
            result_list[index] = holdem_functions.detect_hand(hole_card, board,
                                                     suit_histogram, histogram)
        # Find the winner of the hand and tabulate results
        winner_index = holdem_functions.compare_hands(result_list)
        winner_list[winner_index] += 1
        # Increment what hand each player made
        for index, result in enumerate(result_list):
            result_histograms[index][result[0]] += 1
    holdem_functions.print_results(hole_cards, winner_list, result_histograms)

if __name__ == '__main__':
    start = time.time()
    main()
    print "\nTime elapsed(seconds): ", time.time() - start
