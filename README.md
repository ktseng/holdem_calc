Holdem Calculator
=================

The Holdem Calculator library calculates the probability that a certain Texas Hold'em hand will win by running a Monte Carlo simulation. It also shows you how likely each set of hole cards is to make a certain poker hand. Numbers are generally accurate to the nearest percent. Accuracy can be improved by increasing the number of simulations that are run, but this will result in a longer running time.

Usage
-----

	$ python holdem_calc.py As Ks Qc Qd
	Winning Percentages:
	(As, Ks) :  0.45821
	(Qc, Qd) :  0.53795
	Ties:  0.00384

	Player1 Histogram:
	High Card :  0.17454
	Pair :  0.43063
	Two Pair :  0.22761
	Three of a Kind :  0.04535
	Straight :  0.02194
	Flush :  0.07397
	Full House :  0.02399
	Four of a Kind :  0.00135
	Straight Flush :  3e-05
	Royal Flush :  0.00059

	Player2 Histogram:
	High Card :  0.0
	Pair :  0.35173
	Two Pair :  0.38824
	Three of a Kind :  0.12356
	Straight :  0.01602
	Flush :  0.02289
	Full House :  0.08773
	Four of a Kind :  0.00964
	Straight Flush :  8e-05
	Royal Flush :  0.00011


	Time elapsed(seconds):  1.7265150547

This usage pattern also applies for parallel_holdem_calc.py. You can add in as many players as you want, as long as the number of hole cards you provide is an even number.
