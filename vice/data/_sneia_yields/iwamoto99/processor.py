"""
Argv: 
===== 
1) 			The name of the element to produce the table for 
"""

import sys 

with open("table.dat", 'r') as f: 
	isotopes = []
	W7 = []
	W70 = []
	WDD1 = []
	WDD2 = []
	WDD3 = [] 
	CDD1 = [] 
	CDD2 = [] 
	line = f.readline() 
	while line[0] == '#': 
		line = f.readline() 
	while line != "": 
		line = line.split()
		if line[0][2:] == sys.argv[1]: 
			isotopes.append("%s%s" % (sys.argv[1].lower(), line[0][:2]))
			W7.append(float(line[2])) 
			W70.append(float(line[3])) 
			WDD1.append(float(line[4])) 
			WDD2.append(float(line[5])) 
			WDD3.append(float(line[6])) 
			CDD1.append(float(line[7])) 
			CDD2.append(float(line[8]))
		else:
			pass
		line = f.readline() 
	f.close() 

def write_to_file(filename, isotopes, arr): 
	with open(filename, 'w') as f: 
		f.write("# isotope\tMass yield (Msun)\n") 
		for i in range(len(isotopes)): 
			f.write("%s\t%.2e\n" % (isotopes[i], arr[i]))
		f.write("\n") 
		f.close() 

write_to_file("W7/%s.dat" % (sys.argv[1].lower()), isotopes, W7)
write_to_file("W70/%s.dat" % (sys.argv[1].lower()), isotopes, W70)
write_to_file("WDD1/%s.dat" % (sys.argv[1].lower()), isotopes, WDD1)
write_to_file("WDD2/%s.dat" % (sys.argv[1].lower()), isotopes, WDD2)
write_to_file("WDD3/%s.dat" % (sys.argv[1].lower()), isotopes, WDD3)
write_to_file("CDD1/%s.dat" % (sys.argv[1].lower()), isotopes, CDD1)
write_to_file("CDD2/%s.dat" % (sys.argv[1].lower()), isotopes, CDD2)




