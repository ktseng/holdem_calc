Holdem Calculator
=================

The Holdem Calculator library calculates the probability that a certain Texas Hold'em hand will win by running a Monte Carlo simulation. It also shows you how likely each set of hole cards is to make a certain poker hand. Numbers are generally accurate to the nearest percent. Accuracy can be improved by increasing the number of simulations that are run, but this will result in a longer running time.

Usage
-----

	$ python holdem_calc.py Ad Kd Qc Qs
	Winning Percentages:
	(2d, 3d) :  0.46148
	(4c, 4s) :  0.53427
	Ties:  0.00425

	Player1 Histogram:
	High Card :  0.17318
	Pair :  0.42858
	Two Pair :  0.23224
	Three of a Kind :  0.04573
	Straight :  0.02197
	Flush :  0.07181
	Full House :  0.02427
	Four of a Kind :  0.0014
	Straight Flush :  2e-05
	Royal Flush :  0.0008

	Player2 Histogram:
	High Card :  0.0
	Pair :  0.34864
	Two Pair :  0.39275
	Three of a Kind :  0.12333
	Straight :  0.01545
	Flush :  0.02333
	Full House :  0.08706
	Four of a Kind :  0.00931
	Straight Flush :  9e-05
	Royal Flush :  4e-05


	Time elapsed(seconds):  1.56669712067

This usage pattern also applies for parallel_holdem_calc.py. You can add in as many players as you want, as long as the number of hole cards you provide is an even number.
