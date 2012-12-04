import random
import time
from holdem_functions import *
from multiprocessing import Process, Array

deck = None
num_iterations = 1000000

# Multiprocessing state variables
num_processes = 8
winner_list = None
result_histograms = None
thread_iters = num_iterations / num_processes


# Generating boards
def generate_boards():
    for iteration in xrange(thread_iters):
        yield random.sample(deck, 5)


# Separated function for each thread to execute while running
def simulation_loop(num_players, deck, hole_cards, proc_id):
    # Create results data structures which tracks results of comparisons
    # result_list: list of the best possible poker hand for each pair of
    #    hole cards for a given board
    result_list = []
    for player in xrange(num_players):
        result_list.append([])
    # Run num_iterations simulations
    for board in generate_boards():
        # Find the best possible poker hand given the created board and the
        # hole cards and save them in the results data structures
        for index, hole_card in enumerate(hole_cards):
            result_list[index] = detect_hand(hole_card, board)
        # Find the winner of the hand and tabulate results
        winner_index = compare_hands(result_list)
        winner_list[proc_id * (num_players + 1) + winner_index] += 1
        # Increment what hand each player made
        for index, result in enumerate(result_list):
            result_histograms[10 * (proc_id * num_players + index)
                                                          + result[0]] += 1


def main():
    # Data structures:
    # 1) result_histograms: a list for each player that shows the number of
    #    times each type of poker hand (e.g. flush, straight) was gotten
    # 2) winner_list: number of times each player wins the given round
    global winner_list, result_histograms, deck
    random.seed(time.time())
    # Parse command line arguments into hole cards and create deck
    hole_cards = parse_cards()
    num_players = len(hole_cards)
    deck = generate_deck(hole_cards)
    # Create data structures to manage multiple processes
    winner_list = Array('i', num_processes * (num_players + 1))
    result_histograms = Array('i', num_processes * num_players * 10)
    processes = [None] * num_processes
    # Create, start, and join processes
    for proc_id in xrange(num_processes):
        processes[proc_id] = Process(target=simulation_loop,
                                     args=(num_players, deck, hole_cards,
                                           proc_id))
        processes[proc_id].start()
    for proc_id in xrange(num_processes):
        processes[proc_id].join()
    # Tallying and printing results
    combined_winner_list, combined_histograms = [0] * (num_players + 1), []
    for player in xrange(num_players):
        combined_histograms.append([0] * 10)
    # Go through each parallel data structure and aggregate results
    for index, element in enumerate(winner_list):
        combined_winner_list[index % (num_players + 1)] += element
    for index, element in enumerate(result_histograms):
        combined_histograms[(index / 10) % num_players][index % 10] += element
    # Print results
    print_results(hole_cards, combined_winner_list, combined_histograms)

if __name__ == '__main__':
    start = time.time()
    main()
    print "\nTime elapsed(seconds): ", time.time() - start
