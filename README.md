Holdem Calculator
=================

The Holdem Calculator library calculates the probability that a certain Texas Hold'em hand will win. This probability is approximated by running a Monte Carlo method or calculated exactly by simulating the set of all possible hands. The Holdem Calculator also shows how likely each set of hole cards is to make a certain poker hand. The default Monte Carlo simulations are generally accurate to the nearest percent. Accuracy can be improved by increasing the number of simulations that are run, but this will result in a longer running time.

Usage
-----
Default use case:

	$ python holdem_calc.py Ad Kd Qc Qs
	Winning Percentages:
	(Ad, Kd) :  0.46148
	(Qc, Qs) :  0.53427
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

Multiplayer use case:

	$ python holdem_calc.py As Ks Td Jd 4h 4c
	Winning Percentages:
	(As, Ks) :  0.38166
	(Td, Jd) :  0.33029
	(4h, 4c) :  0.2853
	Ties:  0.00275

	Player1 Histogram:
	High Card :  0.16582
	Pair :  0.4193
	Two Pair :  0.2321
	Three of a Kind :  0.04763
	Straight :  0.02355
	Flush :  0.08369
	Full House :  0.02572
	Four of a Kind :  0.00146
	Straight Flush :  1e-05
	Royal Flush :  0.00072

	Player2 Histogram:
	High Card :  0.13874
	Pair :  0.38832
	Two Pair :  0.22959
	Three of a Kind :  0.04561
	Straight :  0.0889
	Flush :  0.07811
	Full House :  0.02649
	Four of a Kind :  0.00162
	Straight Flush :  0.00195
	Royal Flush :  0.00067

	Player3 Histogram:
	High Card :  0.0
	Pair :  0.34242
	Two Pair :  0.38102
	Three of a Kind :  0.12639
	Straight :  0.02482
	Flush :  0.02576
	Full House :  0.08957
	Four of a Kind :  0.00981
	Straight Flush :  0.00021
	Royal Flush :  0.0


	Time elapsed(seconds):  2.0515730381

Exact calculation:

	$ python holdem_calc.py As Ac 7d 8d -e
	Winning Percentages:
	(As, Ac) :  0.768322681019
	(7d, 8d) :  0.228739756492
	Ties:  0.0029375624889

	Player1 Histogram:
	High Card :  0.0
	Pair :  0.354008400378
	Two Pair :  0.391353404536
	Three of a Kind :  0.122024476962
	Straight :  0.0131553742793
	Flush :  0.0226425915024
	Full House :  0.0875755706931
	Four of a Kind :  0.00912221194367
	Straight Flush :  6.5408946075e-05
	Royal Flush :  5.25607602388e-05

	Player2 Histogram:
	High Card :  0.14545489586
	Pair :  0.393180182958
	Two Pair :  0.223752908362
	Three of a Kind :  0.0444173464525
	Straight :  0.0941649380017
	Flush :  0.0710019949729
	Full House :  0.0243624963791
	Four of a Kind :  0.00141330044198
	Straight Flush :  0.00225076855512
	Royal Flush :  1.1680168942e-06


	Time elapsed(seconds):  19.6590108871

Board supplied:

	$ python holdem_calc.py As Ac 7d 8d -b 6d 9d 2h
	Winning Percentages:
	(As, Ac) :  0.437373737374
	(7d, 8d) :  0.562626262626
	Ties:  0.0

	Player1 Histogram:
	High Card :  0.0
	Pair :  0.518181818182
	Two Pair :  0.384848484848
	Three of a Kind :  0.0686868686869
	Straight :  0.0
	Flush :  0.0
	Full House :  0.0272727272727
	Four of a Kind :  0.0010101010101
	Straight Flush :  0.0
	Royal Flush :  0.0

	Player2 Histogram:
	High Card :  0.106060606061
	Pair :  0.241414141414
	Two Pair :  0.0787878787879
	Three of a Kind :  0.0131313131313
	Straight :  0.19696969697
	Flush :  0.275757575758
	Full House :  0.0
	Four of a Kind :  0.0
	Straight Flush :  0.0878787878788
	Royal Flush :  0.0


	Time elapsed(seconds):  0.0137040615082

Command Line Options
--------------------

	-h, --help            show this help message and exit
	-b [card [card ...]]  Add board cards
	-e, --exact           Find exact odds by enumerating every possible board
	-n N                  Run N Monte Carlo simulations


This usage pattern also applies for parallel_holdem_calc.py. You can add in as many players as you want, as long as the number of hole cards you provide is a non-zero even number. Additionally, you
can provide a board for common cards that are provided to all opponents.
