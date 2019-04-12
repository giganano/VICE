"""
ARGV:
=====
1)		Element symbol
"""

import sys
import os

masses = [13, 15, 20, 25, 30, 40, 60, 80, 120]
FeH = [-3, -2, -1, 0]
vel = [0, 150, 300]

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

for i in range(len(FeH)):
	for j in range(len(vel)):
		with open("./table8.dat", 'r') as f1:
			with open("./FeH%d/v%d/%s.dat" % (FeH[i], vel[j], 
				sys.argv[1].lower()), 'w') as f2:

				line = f1.readline()
				while line != "":
					yields = []
					isotopes = []
					line = line.split()
					if (is_element(sys.argv[1], line[2]) and 
						int(line[0]) == vel[j] and int(line[1]) == FeH[i]):
						while sys.argv[1] in line[2]:
							yields.append([float(x) for x in line[3:]])
							isotopes.append(line[2].lower())
							line = f1.readline()
							if line != "": 
								line = line.split()
							else:
								break
						break
					else:
						line = f1.readline()
						continue

				if len(isotopes) == 0: 
					f2.close() 
					os.system("rm -f ./FeH%d/v%d/%s.dat" % (FeH[i], vel[j], 
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



