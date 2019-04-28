# coding: utf-8
"""
ARGV:
=====
1) 		The elemental symbol 
"""
import struct
import sys 

models = ["N1", "N3", "N5", "N10", "N20", "N40", "N100H", "N100", 
	"N100L", "N150", "N200", "N300C", "N1600", "N1600C", "N100_Z0P5", 
	"N100_Z0P1", "N100_Z0P01"]
isotopes = []
yields = 17 * [None] # one for each model 
for i in range(17): 
	yields[i] = []

with open("table.dat", 'r') as f: 
	line = f.readline() 
	while line != "": 
		line = line.split() 
		if line[0][2:] == sys.argv[1]: 
			isotopes.append("%s%d" % (sys.argv[1].lower(), 
				float(line[0][:2])))
			for i in range(17): 
				yields[i].append(float(line[i + 1]))
		else:
			pass
		line = f.readline() 

# print(isotopes)
# print(yields)
# print(float(yields[0][0]))

for i in range(17): 
	with open("%s/%s.dat" % (models[i], sys.argv[1].lower()), 'w') as f: 
		f.write("# isotope\tMass yield (Msun)\n") 
		for j in range(len(isotopes)): 
			f.write("%s\t%.2e\n" % (isotopes[j], yields[i][j]))
		f.write("\n")
		f.close()




