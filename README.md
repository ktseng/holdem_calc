Holdem Calculator
=================

The Holdem Calculator library calculates the probability that a certain Texas Hold'em hand will win. This probability is approximated by running a Monte Carlo method or calculated exactly by simulating the set of all possible hands. The Holdem Calculator also shows how likely each set of hole cards is to make a certain poker hand. The default Monte Carlo simulations are generally accurate to the nearest percent. Accuracy can be improved by increasing the number of simulations that are run, but this will result in a longer running time.

Command Line Options
--------------------

	-h, --help            show this help message and exit
	-b [card [card ...]], --board [card [card ...]]
	                      Add board cards
	-e, --exact           Find exact odds by enumerating every possible board
	-n N                  Run N Monte Carlo simulations
	-i INPUT, --input INPUT
	                      Read hole cards and boards from an input file.
	                      Commandline arguments for hole cards and board will be
	                      ignored

Usage
-----
I've listed a few examples showing how to use the Holdem Calculator. Note that you can mix and match command line options to suit your needs. See the bottom example in this section to see how to use the multiprocess Holdem Calculator for faster computations.

### Default use case:

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

### Multiplayer use case:

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

### Exact calculation:

	$ python holdem_calc.py As Ac 7d 8d --exact
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

### Board supplied:

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

### Input file supplied:

In order to calculate multiple hands in a single run, the user has the choice to allow Holdem Calculator to read from an input file. Each line of the input file should represent a single calculation. Hole cards and boards should be separated using a "|" divider.

	$ cat input_file
	Ad As Td Jd
	Ad As Td Jd | 8d 9d 2c

	$ python holdem_calc.py --input input_file --exact
	Winning Percentages:
	(Ad, As) :  0.791864061522
	(Td, Jd) :  0.203947429896
	Ties:  0.00418850858259

	Player1 Histogram:
	High Card :  0.0
	Pair :  0.358631411245
	Two Pair :  0.393626365412
	Three of a Kind :  0.122320569245
	Straight :  0.0115435109653
	Flush :  0.0170863351368
	Full House :  0.0875755706931
	Four of a Kind :  0.00912221194367
	Straight Flush :  6.71609714163e-05
	Royal Flush :  2.68643885665e-05

	Player2 Histogram:
	High Card :  0.1535743653
	Pair :  0.406777067624
	Two Pair :  0.22637510629
	Three of a Kind :  0.0449108335903
	Straight :  0.0865465478093
	Flush :  0.0543390659603
	Full House :  0.0243624963791
	Four of a Kind :  0.00141330044198
	Straight Flush :  0.0017000485895
	Royal Flush :  1.1680168942e-06

	-----------------------------------
	Winning Percentages:
	(Ad, As) :  0.473737373737
	(Td, Jd) :  0.526262626263
	Ties:  0.0

	Player1 Histogram:
	High Card :  0.0
	Pair :  0.49696969697
	Two Pair :  0.377777777778
	Three of a Kind :  0.0686868686869
	Straight :  0.0
	Flush :  0.0282828282828
	Full House :  0.0272727272727
	Four of a Kind :  0.0010101010101
	Straight Flush :  0.0
	Royal Flush :  0.0

	Player2 Histogram:
	High Card :  0.121212121212
	Pair :  0.256565656566
	Two Pair :  0.0787878787879
	Three of a Kind :  0.0131313131313
	Straight :  0.20303030303
	Flush :  0.239393939394
	Full House :  0.0
	Four of a Kind :  0.0
	Straight Flush :  0.0878787878788
	Royal Flush :  0.0

	-----------------------------------

	Time elapsed(seconds):  16.41842103

### Unknown Hole Cards:

Compute how likely a hand is to win against a random pair of hole cards. You can only specify one set of hole cards as unknown.
**Note:** Performing calculations with unknown hole cards takes an excessively long time if community cards are not specified.

	$ python holdem_calc.py As Ks ? ? -b Ac 2h 6c
	Winning Percentages:
	(As, Ks) :  0.858660611667
	(?, ?) :  0.135034900345
	Ties:  0.00630448798811

	Player1 Histogram:
	High Card :  0.0
	Pair :  0.532839962997
	Two Pair :  0.374653098982
	Three of a Kind :  0.0666049953747
	Straight :  0.0
	Flush :  0.0
	Full House :  0.0249768732655
	Four of a Kind :  0.000925069380204
	Straight Flush :  0.0
	Royal Flush :  0.0

	Player2 Histogram:
	High Card :  0.241033835113
	Pair :  0.470249208085
	Two Pair :  0.185989403751
	Three of a Kind :  0.0336052476663
	Straight :  0.0185462394528
	Flush :  0.0378829927396
	Full House :  0.0121043926779
	Four of a Kind :  0.000543828665938
	Straight Flush :  3.9245367645e-05
	Royal Flush :  5.60648109214e-06


	Time elapsed(seconds):  10.9187510014

### Multiprocess Holdem Calculator:
Takes the same command line options but utilizes multicore processors to increase the speed of computation.
**Windows users:** Due to the process forking mechanism in Windows, parallel_holdem_calc might be slower than expected.

	$ python parallel_holdem_calc.py As Ah Td Jd --exact
	Winning Percentages:
	(As, Ah) :  0.781151594577
	(Td, Jd) :  0.215486268793
	Ties:  0.00336213662994

	Player1 Histogram:
	High Card :  0.0
	Pair :  0.355117432419
	Two Pair :  0.391827619395
	Three of a Kind :  0.122154710846
	Straight :  0.0114418934955
	Flush :  0.022642007494
	Full House :  0.0875755706931
	Four of a Kind :  0.00912221194367
	Straight Flush :  6.65769629692e-05
	Royal Flush :  5.19767517917e-05

	Player2 Histogram:
	High Card :  0.148343401639
	Pair :  0.398811192405
	Two Pair :  0.224704842131
	Three of a Kind :  0.0446024771302
	Straight :  0.0845083583289
	Flush :  0.071000826956
	Full House :  0.0243624963791
	Four of a Kind :  0.00141330044198
	Straight Flush :  0.00167435221783
	Royal Flush :  0.000578752371074


	Time elapsed(seconds):  11.5955700874

### Library Calls:
If you want to use Holdem Calculator as a library, you can import holdem_calc or parallel_holdem_calc and call calculate(). The order of arguments to calculate() are as follows:

1. Board: These are the community cards supplied to the calculation. This is in the form of a list of strings, with each string representing a card. If you do not want to specify community cards, you can set board to be None. Example: ["As", "Ks", "Jd"]
2. Exact: This is a boolean which is True if you want an exact calculation, and False if you want a Monte Carlo simulation.
3. Number of Simulations: This is the number of iterations run in the Monte Carlo simulation. Note that this parameter is ignored if Exact is set to True. **This number must be positive, even if Exact is set to true.**
4. Input File: The name of the input file you want Holdem Calculator to read from. Mark as None, if you do not wish to read from a file. **If Input File is set, library calls will not return anything.**
5. Hole Cards: These are the hole cards for each of the players. This is in the form of a list of strings, with each string representing a card. Example: ["As", "Ks", "Jd", "Td"]
6. Verbose: This is a boolean which is True if you want Holdem Calculator to print the results.

Calls to calculate() return a list of floats. The first element in the list corresponds to the probability that a tie takes place. Each element after that corresponds to the probability one of the hole cards the user provides wins the hand. These probabilities occur in the order in which you list them.


	$ cat example.py
	import holdem_calc
	import parallel_holdem_calc

	print holdem_calc.calculate(["As", "Ks", "Jd"], True, 1, None, ["8s", "7s", "Qc", "Th"], False)
	print parallel_holdem_calc.calculate(None, True, 1, None, ["8s", "7s", "Ad", "Ac"], False)

	$ python example.py
	[0.00404040404040404, 0.36363636363636365, 0.6323232323232323]
	[0.0029375624889038396, 0.2287397564918379, 0.7683226810192583]

## Copyright

Copyright (c) 2013 Kevin Tseng. See [LICENSE](https://github.com/ktseng/holdem_calc/blob/master/LICENSE) for details.
