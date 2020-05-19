""" 
NKT13 processor 

ARGV 
==== 
1) 		Elemental symbol 
""" 

import sys 
import os 

z_dirs = {
	0: 			"FeH-inf", 
	0.001: 		"FeH-1p15", 
	0.004: 		"FeH-0p54", 
	0.008: 		"FeH-0p24", 
	0.02: 		"FeH0p15", 
	0.05: 		"FeH0p55" 
}

def get_yields(filestream): 
	line = filestream.readline() 
	while not line.startswith("M     "): 
		line = filestream.readline() 
	# line = filestream.readline() 
	masses = [float(i) for i in line.split()[1:]] 
	while not line.startswith(sys.argv[1]): 
		line = filestream.readline() 
	isotopes = [] 
	yields = [] 
	while line.startswith(sys.argv[1]) and line != "": 
		isotopes.append("%s%d" % (sys.argv[1], int(line.split()[1]))) 
		yields.append([float(i) for i in line.split()[2:]]) 
		line = f.readline() 
		print(line) 
	# yields = [list(i) for i in zip(masses, yields)] 
	# print(yields) 
	# print(len(yields)) 
	return [masses, isotopes, yields]  


def write_yields(outstream, masses, isotopes, yields): 
	outstream.write("# Units are Msun\n") 
	outstream.write("# M_init\t") 
	for i in isotopes: 
		outstream.write("%s\t" % (i.lower())) 
	outstream.write("\n8\t")
	for i in isotopes: 
		outstream.write("0\t") 
	outstream.write("\n") 
	for i in range(len(masses)): 
		if masses[i] > 8: 
			outstream.write("%g\t" % (masses[i])) 
			for j in range(len(isotopes)): 
				 outstream.write("%e\t" % (yields[j][i])) 
			outstream.write("\n") 
		else: 
			continue 
	outstream.close() 


if __name__ == "__main__": 
	with open("ck13.dat", 'r') as f: 
		for i in z_dirs.keys(): 
			masses, isotopes, yields = get_yields(f) 
			with open("%s/v0/%s.dat" % (z_dirs[i], sys.argv[1].lower()), 
				'w') as out: 
				write_yields(out, masses, isotopes, yields) 
		f.close() 

