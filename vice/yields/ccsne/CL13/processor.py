"""
ARGV:
=====
1)		The elemental symbol
"""

import sys
import os

mass = [13, 15, 20, 25, 30, 40, 60, 80, 120]

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

def get_isotope(string):
	a = "".join([i for i in string if i.isdigit()])
	el = "".join([i for i in string if not i.isdigit()])
	return "%s%s" % (el, a)

if __name__ == "__main__":
	for rot in ["v0", "v300"]:
		with open("./FeH0/%s/table.dat" % (rot), 'r') as f1:
			with open("FeH0/%s/%s.dat" % (rot, sys.argv[1].lower()), 'w') as f2: 
				line = f1.readline()
				yields = []
				isotopes = []
				while line != "":
					line = line.split()
					if is_element(sys.argv[1], line[1]): 
						yields.append([float(i) for i in line[2:]])
						isotopes.append(get_isotope(line[1]))
					else:
						pass
					line = f1.readline()

				if len(isotopes) == 0: 
					f2.close()
					os.system("rm -f FeH0/%s/%s.dat" % (rot, sys.argv[1].lower()))
				else:
					f2.write("# Units are Msun\n")
					f2.write("# M_init\t")
					for i in range(len(isotopes)):
						f2.write("%s\t" % (isotopes[i]))
					f2.write("\n8\t")
					for i in range(len(isotopes)):
						f2.write("0\t")
					f2.write("\n")
					for j in range(len(mass)):
						f2.write("%d\t" % (mass[j]))
						for i in range(len(isotopes)):
							f2.write("%.1e\t" % (yields[i][j]))
						f2.write("\n")
					f2.close()
			f1.close()


