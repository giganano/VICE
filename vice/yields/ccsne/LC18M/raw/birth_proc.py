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

			in_section = False

			for line in f1:
				line = line.split()
				if line[0] == "ele":
					if (is_element(FeH_label[i], line[4]) and
						int(digits(line[4])[3:])==vel):
						in_section = True
					elif in_section:
						break

				if line[0].lower() in _RECOGNIZED_ISOTOPES_ and in_section:
					print(line[0], line[3])
					f2.write('%s \t %2.3e\n' % (line[0].lower(), float(line[3])))
				else:
					pass
