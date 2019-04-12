"""
ARGV:
=====
1)		Element symbol
"""

import sys
import os

masses = [13, 15, 20, 25, 30, 35]
Z = [0, 1e-6, 1e-4, 1e-3, 6e-3, 2e-2]
dirs = dict(zip(Z, ["FeH-inf", "FeH-4", "FeH-2", "FeH-1", "FeH-0p37", 
	"FeH0p15"]))
strs = dict(zip(Z, ["0e+00", "1e-06", "1e-04", "1e-03", "6e-03", "2e-02"]))

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

for i in range(len(Z)):
	with open("./yields.dat", 'r') as f1:
		with open("./%s/v0/%s.dat" % (dirs[Z[i]], sys.argv[1].lower()), 
			'w') as f2: 

			line = f1.readline()
			yields = []
			isotopes = []
			while line != "":
				line = line.split()
				if (is_element(sys.argv[1], line[4]) and line[1] == strs[Z[i]]):
					yields.append([float(x) for x in line[5:]])
					isotopes.append("%s%d" % (sys.argv[1].lower(), int(line[3])))
				else:
					pass
				line = f1.readline()

			if len(isotopes) == 0: 
				f2.close() 
				os.system("rm -f ./%s/v0/%s.dat" % (dirs[Z[i]], 
					sys.argv[1].lower()))
			else:
				f2.write("# Units are Msun\n")
				f2.write("# M_init\t")
				for k in range(len(isotopes)):
					f2.write("%s\t" % (isotopes[k]))
				f2.write("\n8\t")
				for k in range(len(isotopes)):
					f2.write("0\t")
				f2.write("\n")
				for l in range(len(masses)):
					f2.write("%d\t" % (masses[l]))
					for k in range(len(isotopes)):
						f2.write("%.4e\t" % (yields[k][l]))
					f2.write("\n")
				f2.close()
		f1.close()




