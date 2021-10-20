
import vice
import sys

masses = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 6.5, 7.0]
metallicities = [0.0003, 0.001, 0.002, 0.004, 0.008, 0.014, 0.04]

def pull_yields_given_Z(filename, element):
	columns = {
		"he": [2],
		"c": [4, 5],
		"n": [6],
		"o": [7, 8, 9],
		"ne": [10, 11],
		"na": [12],
		"mg": [13, 14, 15],
		"al": [16],
		"si": [17]
	}
	yields = len(masses) * [0.]
	with open(filename, 'r') as f_in:
		while True:
			line = f_in.readline()
			if line.split()[0] == "init":
				line = f_in.readline()
				break
			else: continue
		while line != "":
			line = [float(_) for _ in line.split()]
			if line[0] in masses: # if all metallicities report a value there
				idx = masses.index(line[0])
				for column in columns[element]: yields[idx] += line[column]
			else: pass
			line = f_in.readline()
		f_in.close()
	return yields


def pull_yields(element):
	yields = []
	for Z in metallicities:
		filename = ("raw_Z%g" % (Z)).replace('.', 'p')
		filename += ".dat"
		yields.append(pull_yields_given_Z(filename, element))
	return yields


def write_yields(element):
	with open("../%s.dat" % (element.lower()), 'w') as f_out:
		yields = pull_yields(element)
		for i in range(len(masses)):
			for j in range(len(metallicities)):
				f_out.write("%g\t%g\t%.5e\n" % (masses[i], metallicities[j],
					yields[j][i] / masses[i]))
		f_out.close()


if __name__ == "__main__": write_yields(sys.argv[1].lower())

