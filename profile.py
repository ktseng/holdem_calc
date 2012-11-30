import cProfile
import pstats
import holdem_calc

# Profiling code
cProfile.run('holdem_calc.main()', 'prof')
p = pstats.Stats('prof')
p.sort_stats('time').print_stats()
