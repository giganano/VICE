"""
ARGV:
=====
1) 		Element symbol 
"""

import sys
import os 

def get_symbol(foo): 
	return "".join([i for i in foo if not i.isdigit()])

zdirs = {
	0: 				"FeH-inf", 
	1.9e-6: 		"FeH-4", 
	1.9e-4: 		"FeH-2", 
	1.9e-3: 		"FeH-1", 
	1.9e-2: 		"FeH0"
}

masses = [7.0000E-01, 1.0000E+00, 1.5000E+00, 1.7500E+00, 2.0000E+00, 
	2.5000E+00, 3.0000E+00, 4.0000E+00, 5.0000E+00, 6.0000E+00, 7.0000E+00, 
	8.0000E+00, 1.0000E+01, 1.1065E+01, 1.2065E+01, 1.3071E+01, 1.5081E+01, 
	1.8098E+01, 1.9000E+01, 2.0109E+01, 2.2119E+01, 2.5136E+01, 3.0163E+01, 
	3.5190E+01, 4.0217E+01]
metallicities = [0, 1.9e-6, 1.9e-4, 1.9e-3, 1.9e-2]

isotopes = [] 
yields = [] 
# z = []


with open("table.dat", 'r') as f: 
	line = f.readline()
	while line != "":
		if get_symbol(line.split()[0]) == sys.argv[1].lower(): 
			isotopes.append(line.split()[0])
			for i in range(5): 
				line = f.readline() 
				# z.append(float(line.split()[0]))
				arr = len(masses) * [0]
				for i in range(len(arr)): 
					line = f.readline()
					arr[i] = float(line.split()[1])
				yields.append(arr)
		else:
			pass
		line = f.readline()
	f.close() 

if len(yields) > 0: 
	for i in range(5): 
		with open("%s/v0/%s.dat" % (zdirs[metallicities[i]], 
			sys.argv[1].lower()), 'w') as f: 
			# The indeces of the elements of yields that are to be written out 
			# for this metallicity 
			indeces = [i]
			while indeces[-1] + 5 < len(yields): 
				indeces.append(indeces[-1] + 5)
			f.write("# Units are Msun\n")
			f.write("# M_init\t")
			for j in isotopes: 
				f.write("%s\t" % (j))
			f.write("\n")
			f.write("8\t") 
			for j in range(len(isotopes)): 
				f.write("0\t") 
			f.write("\n")
			for j in range(len(masses)): 
				f.write("%e\t" % (masses[j]))
				for k in indeces: 
					f.write("%e\t" % (yields[k][j]))
				f.write("\n")
			f.close()
else:
	pass






