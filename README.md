Holdem Calculator
=================

The Holdem Calculator library calculates the probability that a certain Texas Hold'em hand will win by running a Monte Carlo simulation. It also shows you how likely each set of hole cards is to make a certain poker hand. Numbers are generally accurate to the nearest percent. Accuracy can be improved by increasing the number of simulations that are run, but this will result in a longer running time.

Usage
-----

	$ python holdem_calc.py As Ks Qc Qd
	Winning Percentages:
	(As, Ks) :  0.4599
	(Qc, Qd) :  0.53496
	Ties:  0.00514

	Player1 Histogram:
	High Card :  0.17476
	Pair :  0.42977
	Two Pair :  0.23026
	Three of a Kind :  0.0463
	Straight :  0.02188
	Flush :  0.07196
	Full House :  0.02328
	Four of a Kind :  0.00132
	Straight Flush :  5e-05
	Royal Flush :  0.00042

	Player2 Histogram:
	High Card :  0.0
	Pair :  0.35195
	Two Pair :  0.38961
	Three of a Kind :  0.12204
	Straight :  0.01611
	Flush :  0.02272
	Full House :  0.08818
	Four of a Kind :  0.00917
	Straight Flush :  0.00015
	Royal Flush :  7e-05


	Time elapsed(seconds):  2.03514385223

This usage pattern also applies for parallel_holdem_calc.py. You can add in as many players as you want, as long as the number of hole cards you provide is an even number.
