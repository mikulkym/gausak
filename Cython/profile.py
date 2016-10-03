import pstats, cProfile

import pyximport
pyximport.install()

import gaussian

cProfile.runctx("gaussian.main()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()