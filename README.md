Holdem Calculator
=================

The Holdem Calculator library calculates the probability that a certain Texas Hold'em hand will win by running a Monte Carlo simulation. It also shows you how likely each set of hole cards is to make a certain poker hand. Numbers are generally accurate to the nearest percent. Accuracy can be improved by increasing the number of simulations that are run, but this will result in a longer running time.

Usage
-----

	$ python holdem_calc.py As Ks Qc QdWinning Percentages:
	(As, Ks) :  0.46104
	(Qc, Qd) :  0.53494
	Ties:  0.00402

	Player1 Histogram:
	High Card :  0.1768
	Pair :  0.42739
	Two Pair :  0.22936
	Three of a Kind :  0.04581
	Straight :  0.02149
	Flush :  0.0725
	Full House :  0.02441
	Four of a Kind :  0.00156
	Straight Flush :  5e-05
	Royal Flush :  0.00063

	Player2 Histogram:
	High Card :  0.0
	Pair :  0.35462
	Two Pair :  0.38988
	Three of a Kind :  0.1206
	Straight :  0.01591
	Flush :  0.02278
	Full House :  0.08671
	Four of a Kind :  0.00923
	Straight Flush :  0.00018
	Royal Flush :  9e-05


	Time elapsed(seconds):  2.17448210716

This usage pattern also applies for parallel_holdem_calc.py. You can add in as many players as you want, as long as the number of hole cards you provide is an even number.
