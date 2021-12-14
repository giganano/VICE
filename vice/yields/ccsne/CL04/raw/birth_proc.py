from vice._globals import _RECOGNIZED_ISOTOPES_

Z = [0, 1E-6, 1E-4, 1E-3, 6E-3, 2E-2]
Y = [0.23, 0.23, 0.23, 0.23, 0.26, 0.285]
X = [1-(z+y) for z,y in zip(Z,Y)]
print(X)

# Values form AG1989
elem, solar = [], []
with open('Solar_isotopes.txt', 'r') as f:
	for line in f:
		line = line.split()
		elem.append(line[0])
		solar.append(float(line[1]))

# VICE info
outfile = '../'
out_feh = ['FeH-inf', 'FeH-4','FeH-2','FeH-1','FeH-0p37', 'FeH0p15']

solar_z = 1.886E-2
solar_y = 27.431E-2
solar_x = 70.683E-2

ratio = [z/solar_z for z in Z]

for i in range(6):
	scaled = [s*ratio[i] for s in solar]
	with open(outfile+out_feh[i]+'/birth_composition.dat', 'w') as f:
		f.write('%s \t %1.3e \n' % ('he4', Y[i]))
		for e, abn in zip(elem, scaled):
			if e.lower() in _RECOGNIZED_ISOTOPES_:
				f.write('%s \t %1.3e \n' % (e.lower(), abn))
	f.close()
