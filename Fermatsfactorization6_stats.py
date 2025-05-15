import pstats
from pstats import SortKey

p = pstats.Stats('Fermatsfactorization6_output.stats')
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(10)
