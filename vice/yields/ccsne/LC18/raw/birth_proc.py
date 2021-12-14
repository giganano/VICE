"""
LC18 processor
"""

from vice._globals import _RECOGNIZED_ISOTOPES_

file = "tab_yieldsnet_iso_exp.dec"

FeH = [0, -1, -2, -3]
FeH_label = ['a','b','c','d']
vel = 0

def is_element(symbol, test):
	return symbol.lower() == "".join([i for i in test if not i.isdigit(
		)]).lower()

def digits(string):
	return "".join([i for i in string if i.isdigit()])


for i in range(len(FeH)):
	print('\n', FeH[i], vel)
	with open(file,'r') as f1:
		with open('../FeH%d/birth_composition.dat' % (FeH[i]), 'w+') as f2:
			line = f1.readline()
			while line != "":
				line = line.split()
				if (is_element(FeH_label[i], line[4]) and
							int(digits(line[4])[3:])==vel):
					counter = 141
				if ((line[0].lower() in _RECOGNIZED_ISOTOPES_) and
					counter>0):
					print(line[0], line[3])
					f2.write('%s \t %2.3e\n' % (line[0].lower(), float(line[3])))
				else:
					pass
				line = f1.readline()
				counter = counter-1
		f2.close()
	f1.close()
