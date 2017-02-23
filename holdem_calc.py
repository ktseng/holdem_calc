import time
import holdem_functions
import holdem_argparser


def main():
    hole_cards, num, exact, board, file_name = holdem_argparser.parse_args()
    if file_name:
        input_file = open(file_name, 'r')
        for line in input_file:
            hole_cards, board = holdem_argparser.parse_file_args(line)
            deck = holdem_functions.generate_deck(hole_cards, board)
            run_simulation(hole_cards, num, exact, board, deck)
            print "-----------------------------------"
        input_file.close()
    else:
        deck = holdem_functions.generate_deck(hole_cards, board)
        run_simulation(hole_cards, num, exact, board, deck)

def run_simulation(hole_cards, num_iterations, exact, given_board, deck):
    num_players = len(hole_cards)
    # Create results data structures which tracks results of comparisons
    # 1) result_histograms: a list for each player that shows the number of
    #    times each type of poker hand (e.g. flush, straight) was gotten
    # 2) winner_list: number of times each player wins the given round
    # 3) result_list: list of the best possible poker hand for each pair of
    #    hole cards for a given board
    result_list, winner_list = [None] * num_players, [0] * (num_players + 1)
    result_histograms = []
    for _ in xrange(num_players):
        result_histograms.append([0] * len(holdem_functions.hand_rankings))
    # Choose whether we're running a Monte Carlo or exhaustive simulation
    board_length = 0 if given_board is None else len(given_board)
    # When a board is given, exact calculation is much faster than Monte Carlo
    # simulation, so default to exact if a board is given
    if exact or given_board is not None:
        generate_boards = holdem_functions.generate_exhaustive_boards
    else:
        generate_boards = holdem_functions.generate_random_boards
    # Run simulations
    for remaining_board in generate_boards(deck, num_iterations, board_length):
        # Generate a new board
        if given_board:
            board = given_board[:]
            board.extend(remaining_board)
        else:
            board = remaining_board
        # Find the best possible poker hand given the created board and the
        # hole cards and save them in the results data structures
        suit_histogram, histogram, max_suit = (
            holdem_functions.preprocess_board(board))
        for index, hole_card in enumerate(hole_cards):
            result_list[index] = (
                holdem_functions.detect_hand(hole_card, board, suit_histogram,
                                             histogram, max_suit))
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
