"""
ARGV:
=====
1)		Element symbol
"""

import os

from vice.core.dataframe._builtin_dataframes import stable_isotopes
import vice.elements

masses = [13, 15, 20, 25, 30, 35]
Z = [0, 1e-6, 1e-4, 1e-3, 6e-3, 2e-2]
dirs = dict(zip(Z, ["FeH-inf", "FeH-4", "FeH-2", "FeH-1", "FeH-0p37",
	"FeH0p15"]))
strs = dict(zip(Z, ["0e+00", "1e-06", "1e-04", "1e-03", "6e-03", "2e-02"]))

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

def digits(string):
	return "".join([i for i in string if i.isdigit()])

def decay(string):
	unstable = ['ni56', 'al26']
	stable = ['fe56', 'mg26']
	if string.lower() in unstable:
		return stable[unstable.index(string.lower())]
	else:
		return string

def get_symbol(foo):
	# returns the symbol from an isotpe e.g. c12 to c
	return "".join([i for i in foo if not i.isdigit()])

for ele in vice.elements.recognized:
	print(ele)
	for i in range(len(Z)):
		with open("./yields.dat", 'r') as f1:
			with open("../%s/v0/explosive/%s.dat" % (dirs[Z[i]], ele.lower()), 'w') as f2:
				with open("../%s/v0/wind/%s.dat" % (dirs[Z[i]], ele.lower()), 'w') as f3:

					line = f1.readline()
					yields = []
					isotopes = []
					while line != "":
						line = line.split()
						symbol = line[4].lower()
						mass = line[3]
						if ((is_element(ele, get_symbol(decay(symbol+mass))))
							and (line[1] == strs[Z[i]]) and (line[2]=='0.0e+00')
							and (int(digits(decay(symbol+mass))) in stable_isotopes[get_symbol(decay(symbol+mass))])):
							yields.append([float(x) for x in line[5:]])
							isotopes.append("%s%d" % (symbol, int(mass)))
						else:
							pass
						line = f1.readline()

					if len(isotopes) == 0:
						f2.close()
						f3.close()
						os.system("rm -f ../%s/v0/explosive/%s.dat" % (dirs[Z[i]],
							ele.lower()))
						os.system("rm -f ../%s/v0/wind/%s.dat" % (dirs[Z[i]],
							ele.lower()))
					else:
						f2.write("# Units are Msun\n")
						f2.write("# M_init\t")
						f3.write("# Units are Msun\n")
						f3.write("# M_init\t")
						for k in range(len(isotopes)):
							f2.write("%s\t" % (isotopes[k]))
							f3.write("%s\t" % (isotopes[k]))
						f2.write("\n8\t")
						f3.write("\n8\t")
						for k in range(len(isotopes)):
							f2.write("0\t")
							f3.write("0\t")
						f2.write("\n")
						f3.write("\n")
						for l in range(len(masses)):
							f2.write("%d\t" % (masses[l]))
							f3.write("%d\t" % (masses[l]))
							for k in range(len(isotopes)):
								f2.write("%.4e\t" % (yields[k][l]))
								f3.write("%.4e\t" % 0.0)
							f2.write("\n")
							f3.write("\n")
						f2.close()
						f3.close()
			f1.close()
