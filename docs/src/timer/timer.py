"""
Runs VICE integrations at 10^-4 steps in delta t to numerically determine
execution speed from 5x10^-4 to 5x10^-2

ARGV:
=====
1)			The number of elements to run the integration for
2) 			A dummy name for an output object to write to
3) 			The name of the output file
"""

import numpy as np
import vice
import time
import sys
import os

with open(sys.argv[3], 'w') as f:
	print("Timing VICE for N = %d elements..." % (int(sys.argv[1])))

	# write the header
	f.write("# Number of elements: %d\n" % (int(sys.argv[1])))
	f.write("# 1) Timestep Size [Gyr]\n")
	f.write("# 2) Execution time of a 10 Gyr simulation [sec]\n")

	# start at .05 and divide by a small amount until .0005
	dt = 5.e-2
	while dt >= 5.e-4:
		start = time.time()
		vice.singlezone(name = sys.argv[2],
			elements = vice._globals._RECOGNIZED_ELEMENTS_[:int(sys.argv[1])],
			dt = dt).run(np.linspace(0, 10, 201), overwrite = True)
		stop = time.time()
		print("dt = %.5e | T_exec = %.5e seconds" % (dt, stop - start))
		f.write("%.5e\t%.5e\n" % (dt, stop - start))
		dt /= 1.01
	f.close()

