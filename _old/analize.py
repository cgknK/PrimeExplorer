import cProfile
import pstats
from memory_profiler import profile

@profile
def function_to_profile():
    # Kodunuz buraya gelecek

# cProfile ile performans profili oluştur
cProfile.run('function_to_profile()', 'profile_stats')

# Profil istatistiklerini görüntüle
p = pstats.Stats('profile_stats')
p.strip_dirs().sort_stats('cumulative').print_stats()


###########

import cProfile

def my_function():
    # Kodunuz buraya gelecek

# cProfile ile profil oluştur
cProfile.run('my_function()')


###################

