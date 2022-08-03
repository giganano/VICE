"""
LC18 processor

ARGV:
=====
1)		Element symbol
"""

import os
import sys

import vice
from vice.core.dataframe._builtin_dataframes import stable_isotopes

files = ["tab_yieldsnet_iso_exp.dec", "tabwind.dec"]
label = ['explosive','wind']
masses = [13, 15, 20, 25, 30, 40, 60, 80, 120]
FeH = [0, -1, -2, -3]
FeH_label = ['a','b','c','d']
vel = [0, 150, 300]

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

def digits(string):
	return "".join([i for i in string if i.isdigit()])

for ele in vice.elements.recognized:
	print(ele)
	for h in range(len(files)):
		for i in range(len(FeH)):
			for j in range(len(vel)):
				with open(files[h], 'r') as f1:
					os.makedirs("../FeH%d/v%d/%s" % (FeH[i], vel[j],
						label[h]), exist_ok=True)
					with open("../FeH%d/v%d/%s/%s.dat" % (FeH[i], vel[j], label[h],
						ele.lower()), 'w') as f2:

						line = f1.readline()
						while line != "":
							line = line.split()
							#read header and determine if vel and FeH match
							if (is_element(FeH_label[i], line[4]) and
								int(digits(line[4])[3:])==vel[j]):
								counter = 142 #number of entries under each FeH and v
								yields = []
								isotopes = []


							if (
								is_element(ele, line[0]) and (counter > 0)
							) and (
								int(digits(line[2])) in stable_isotopes[ele]
							):

								#print(int(digits(line[2])))
								#print([[float(x) for x in line[4:]]])

								yields.append([float(x) for x in line[4:]])
								isotopes.append(line[2].lower())

							else:
								pass
							line = f1.readline()
							counter = counter-1

						if len(isotopes) == 0:
							f2.close()
							os.system("rm -f ../FeH%d/v%d/%s.dat" % (FeH[i], vel[j],
								ele.lower()))
						else:
							f2.write("# Units are Msun\n")
							f2.write("# M_init\t")
							for k in range(len(isotopes)):
								f2.write("%s\t" % (ele.lower()+isotopes[k]))
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


	# for h in range(len(files)):
	# 	for i in range(len(FeH)):
	# 		for j in range(len(vel)):
	# 			with open("../FeH%d/v%d/explosive/%s.dat" % (FeH[i], vel[j],
	# 			ele.lower()), 'r') as f1:
	# 				with open("../FeH%d/v%d/wind/%s.dat" % (FeH[i], vel[j],
	# 				ele.lower()), 'r') as f2:
	# 					os.makedirs("../FeH%d/v%d/total" % (FeH[i], vel[j],
	# 					), exist_ok=True)
	# 					with open("../FeH%d/v%d/total/%s.dat" % (FeH[i], vel[j],
	# 					ele.lower()), 'w') as f3:

	# 						line1 = f1.readline()
	# 						line2 = f2.readline()

	# 						if line1=="" or line2=="":
	# 							f3.close()
	# 							os.system("rm -f ../FeH%d/v%d/total/%s.dat" % (FeH[i], vel[j],
	# 								ele.lower()))
	# 						else:
	# 							line1 = line1.split()
	# 							line2 = line2.split()


	# 							f3.write("# Units are Msun\n")
	# 							f3.write("# M_init\t")

	# 							for k in range(len(isotopes)):
	# 								f3.write("%s\t" % (ele.lower()+isotopes[k]))

	# 							f3.write("\n8\t")
	# 							for k in range(len(isotopes)):
	# 								f3.write("0\t")
	# 							f3.write("\n")

	# 							while line1[0] == '#' or line1[0] =='8':
	# 								line1 = f1.readline().split()
	# 								line2 = f2.readline().split()

	# 							for l in range(len(masses)):
	# 								f3.write("%d\t" % (masses[l]))

	# 								if (int(line1[0])==masses[l]) and (int(line2[0])==masses[l]):
	# 									for k in range(len(isotopes)):
	# 										yield1 = float(line1[k+1])
	# 										yield2 = float(line2[k+1])
	# 										yield3 = yield1 + yield2
	# 										f3.write("%.4e\t" % (yield3))
	# 								line1 = f1.readline().split()
	# 								line2 = f2.readline().split()

	# 								f3.write("\n")
	# 							f3.close()
	# 					f1.close()
	# 					f2.close()






