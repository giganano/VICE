"""
ARGV:
=====
1)		The name of the element to produce the output file for. 
2)		1 if produced by AGB stars 0 if not
"""

import sys
import os

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

mass = [1, 1.25, 1.5, 1.75, 1.9, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
z = [0.0001, 0.004, 0.008, 0.02]
# with open("./table.dat", 'r') as f1:
# 	mass = []
# 	z = []
# 	line = f1.readline()
# 	while line != "":
# 		line = line.split()
# 		if float(line[1]) not in mass: 
# 			mass.append(float(line[1]))
# 		else:
# 			pass
# 		if float(line[3]) not in z:
# 			z.append(float(line[3]))
# 		else:
# 			pass
# 		line = f1.readline()
# 	f1.close()
# 	mass = sorted(mass)
# 	z = sorted(z)
with open("./table.dat", 'r') as f1:
	with open("%s.dat" % (sys.argv[1].lower()), 'w') as f2:
		yields = len(mass) * [None]
		for i in range(len(mass)):
			yields[i] = len(z) * [0.]
		line = f1.readline()
		while line != "":
			line = line.split()

			if (is_element(sys.argv[1], line[5]) and float(line[1]) in mass and 
				float(line[3]) in z):
				yields[mass.index(float(line[1]))][z.index(
					float(line[3]))] += float(line[7])
			else:
				pass
			line = f1.readline()
		for i in range(len(mass)):
			for j in range(len(z)):
				if int(sys.argv[2]):
					yields[i][j] /= mass[i]
				else:
					yields[i][j] = 0.
		for i in range(len(mass)):
			for j in range(len(z)):
				f2.write("%g\t%g\t%.5e\n" % (mass[i], z[j], yields[i][j]))
		f2.close()
	f1.close()






