"""
The following reads in the single-table format of a FRUITY net yield table and 
produces the output file that needs to be produced for VICE. This file is 
not included within the VICE package

ARGV:
=====
1)		The name of the input file
2)		The name of the output file
"""

import sys

with open(sys.argv[1], 'r') as f1:
	with open(sys.argv[2], 'w') as f2:
		line = f1.readline()
		if line.split()[0] == "Mass":
			line = f1.readline()
		while line != "":
			line = [float(i) for i in line.split()]
			if line[1] in [0.0001, 0.0003, 0.001, 0.002, 0.003, 0.006, 0.008, 
				0.01, 0.014, 0.02]:
				net = sum(line[4:])
				f2.write("%g\t%g\t%.5e\n" % (line[0], line[1], net / line[0]))
			else:
				pass
			line = f1.readline()
		f2.close()
	f1.close()


