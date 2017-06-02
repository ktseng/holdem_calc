import multiprocessing
import time
import holdem_argparser
import holdem_functions


def main():
    hole_cards, num, exact, board, file_name = holdem_argparser.parse_args()
    run(hole_cards, num, exact, board, file_name, True)

def calculate(board, exact, num, input_file, hole_cards, verbose):
    args = holdem_argparser.LibArgs(board, exact, num, input_file, hole_cards)
    hole_cards, n, e, board, filename = holdem_argparser.parse_lib_args(args)
    return run(hole_cards, n, e, board, filename, verbose)

def run(hole_cards, num, exact, board, file_name, verbose):
    if file_name:
        input_file = open(file_name, 'r')
        for line in input_file:
            if line is not None and len(line.strip()) == 0:
                continue
            hole_cards, board = holdem_argparser.parse_file_args(line)
            deck = holdem_functions.generate_deck(hole_cards, board)
            run_simulation(hole_cards, num, exact, board, deck, verbose)
            print "-----------------------------------"
        input_file.close()
    else:
        deck = holdem_functions.generate_deck(hole_cards, board)
        return run_simulation(hole_cards, num, exact, board, deck, verbose)

def run_simulation(hole_cards, num, exact, given_board, deck, verbose):
    num_players = len(hole_cards)
    # Choose whether we're running a Monte Carlo or exhaustive simulation
    board_length = 0 if given_board is None else len(given_board)
    # Create data structures to manage multiple processes:
    # 1) winner_list: number of times each player wins a hand
    # 2) result_histograms: a list for each player that shows the number of
    #    times each type of poker hand (e.g. flush, straight) was gotten
    num_processes = multiprocessing.cpu_count()
    num_poker_hands = len(holdem_functions.hand_rankings)
    num_histograms = num_processes * num_players * num_poker_hands
    winner_list = multiprocessing.Array('i', num_processes * (num_players + 1))
    result_histograms = multiprocessing.Array('i', num_histograms)
    # When a board is given, exact calculation is much faster than Monte Carlo
    # simulation, so default to exact if a board is given
    if exact or given_board is not None:
        generate_boards = holdem_functions.generate_exhaustive_boards
    else:
        generate_boards = holdem_functions.generate_random_boards
    if (None, None) in hole_cards:
        hole_cards_list = list(hole_cards)
        unknown_index = hole_cards.index((None, None))
        deck_list = list(deck)
        pool = multiprocessing.Pool(processes=num_processes,
                                    initializer=unknown_simulation_init,
                                    initargs=(hole_cards_list, unknown_index,
                                              deck_list, generate_boards,
                                              num, board_length, given_board,
                                              winner_list, result_histograms))
        pool.map(unknown_simulation, holdem_functions.generate_hole_cards(deck))
    else:
        find_winner(generate_boards, deck, hole_cards, num, board_length,
                    given_board, winner_list, result_histograms)
    # Go through each parallel data structure and aggregate results
    combined_winner_list, combined_histograms = [0] * (num_players + 1), []
    for _ in xrange(num_players):
        combined_histograms.append([0] * len(holdem_functions.hand_rankings))
    for index, element in enumerate(winner_list):
        combined_winner_list[index % (num_players + 1)] += element
    for index, element in enumerate(result_histograms):
        combined_histograms[(index / num_poker_hands) % num_players][
            (index % num_poker_hands)] += element
    if verbose:
        holdem_functions.print_results(hole_cards, combined_winner_list,
                                       combined_histograms)
    return holdem_functions.find_winning_percentage(combined_winner_list)

def unknown_simulation_init(hole_cards_list, unknown_index, deck_list,
                            generate_boards, num, board_length, given_board,
                            combined_winner_list, combined_result_histograms):
    unknown_simulation.hole_cards_list = hole_cards_list
    unknown_simulation.unknown_index = unknown_index
    unknown_simulation.deck = deck_list
    unknown_simulation.generate_boards = generate_boards
    unknown_simulation.num = num
    unknown_simulation.board_length = board_length
    unknown_simulation.given_board = given_board
    unknown_simulation.combined_winner_list = combined_winner_list
    unknown_simulation.combined_result_histograms = combined_result_histograms

def unknown_simulation(new_hole_cards):
    # Extract parameters
    hole_cards_list = unknown_simulation.hole_cards_list
    unknown_index = unknown_simulation.unknown_index
    deck = unknown_simulation.deck[:]
    generate_boards = unknown_simulation.generate_boards
    num = unknown_simulation.num
    board_length = unknown_simulation.board_length
    given_board = unknown_simulation.given_board
    combined_winner_list = unknown_simulation.combined_winner_list
    combined_result_histograms = unknown_simulation.combined_result_histograms
    # Set simulation variables
    num_players = len(hole_cards_list)
    result_histograms, winner_list = [], [0] * (num_players + 1)
    for _ in xrange(num_players):
        result_histograms.append([0] * len(holdem_functions.hand_rankings))
    hole_cards_list[unknown_index] = new_hole_cards
    deck.remove(new_hole_cards[0])
    deck.remove(new_hole_cards[1])
    # Find winner
    holdem_functions.find_winner(generate_boards, deck, tuple(hole_cards_list),
                                 num, board_length, given_board, winner_list,
                                 result_histograms)
    # Write results to parallel data structure for future tabulation
    proc_name = multiprocessing.current_process().name
    proc_id = int(proc_name.split("-")[-1]) % multiprocessing.cpu_count()
    for index, result in enumerate(winner_list):
        combined_winner_list[proc_id * (num_players + 1) + index] += result
    for histogram_index, histogram in enumerate(result_histograms):
        for index, result in enumerate(histogram):
            combined_result_histograms[len(holdem_functions.hand_rankings) *
                                       (proc_id * num_players + histogram_index)
                                       + index] += result

def find_winner(generate_boards, deck, hole_cards, num, board_length,
                given_board, winner_list, result_histograms):
    num_processes = multiprocessing.cpu_count()
    # Create threadpool and use it to perform hand detection over all boards
    pool = multiprocessing.Pool(processes=num_processes,
                                initializer=simulation_init,
                                initargs=(given_board, hole_cards, winner_list,
                                          result_histograms))
    pool.map(simulation, generate_boards(deck, num, board_length))

# Initialize shared variables for simulation
def simulation_init(given_board, hole_cards, winner_list, result_histograms):
    simulation.given_board = given_board
    simulation.hole_cards = hole_cards
    simulation.winner_list = winner_list
    simulation.result_histograms = result_histograms

# Separated function for each thread to execute while running
def simulation(remaining_board):
    # Extract variables shared through inheritance
    given_board, hole_cards = simulation.given_board, simulation.hole_cards
    winner_list = simulation.winner_list
    result_histograms = simulation.result_histograms
    # Generate a new board
    if given_board:
        board = given_board[:]
        board.extend(remaining_board)
    else:
        board = remaining_board
    num_players = len(hole_cards)
    # Extract process id from the name of the current process
    # Names are of the format: PoolWorker-1 - PoolWorker-n
    proc_name = multiprocessing.current_process().name
    proc_id = int(proc_name.split("-")[-1]) % multiprocessing.cpu_count()
    # Create results data structure which tracks results of comparisons
    result_list = []
    for _ in xrange(num_players):
        result_list.append([])
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
    winner_list[proc_id * (num_players + 1) + winner_index] += 1
    # Increment what hand each player made
    for index, result in enumerate(result_list):
        result_histograms[len(holdem_functions.hand_rankings) *
                          (proc_id * num_players + index) + result[0]] += 1

if __name__ == '__main__':
    start = time.time()
    main()
    print "\nTime elapsed(seconds): ", time.time() - start
