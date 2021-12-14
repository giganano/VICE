"""
CL13 birth processor
"""

from vice._globals import _RECOGNIZED_ISOTOPES_

filein='m013zsun.10'
fileout='../FeH0/birth_composition.dat'

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

def digits(string):
	return "".join([i for i in string if i.isdigit()])

def letter(string):
	return "".join([i for i in string if i.isalpha()])

iso = 'None'
birth = 0
with open(filein,'r') as f1:
	with open(fileout, 'w') as f2:
		line = f1.readline()
		while line != "":
			line = line.split()
			iso = line[0].lower()
			if iso in _RECOGNIZED_ISOTOPES_:
				birth = float(line[3])
			else:
				birth = 0
			if birth>0:
				f2.write('%s \t %2.3e \n' % (iso, birth))
				print('%s \t %2.3e' % (iso, birth))
			line = f1.readline()
		f2.write('%s \t %2.3e \n' % (iso, birth))
		f2.close()
	f1.close()
