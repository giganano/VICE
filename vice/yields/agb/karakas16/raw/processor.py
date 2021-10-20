
import sys
import vice

masses = [1.0, 1.25, 1.5, 1.75, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0,
	4.5, 5.0, 5.5, 6.0, 7.0]
metallicities = [0.0028, 0.007, 0.014, 0.03]
files = {
	0.0028: "yields_z0028.dat",
	0.007: "yield_z007.dat",
	0.014: "yield_z014.dat",
	0.03: "yield_z03.dat"
}


def read_block(file):
	r"""
	Reads in a "block" of yields from one of the input files. The block
	corresponds to the full set of elemental yields for a single mass and
	metallicity.
	"""
	block = ""
	while True:
		line = file.readline()
		block += line
		if line.startswith("#  [Rb/Zr]"):
			line = file.readline()
			block += line
			break
		if line == "": break
	return block


def get_mass_from_block(block):
	r"""
	Pulls the initial stellar mass from the block read from the file.
	"""
	lines = block.split('\n')
	top = lines[0]
	return float(top.split()[4][:-1])


def get_masslost_from_block(block):
	r"""
	Pulls the mass lost due to stellar winds from the black read from the file.
	"""
	lines = block.split('\n')
	second = lines[1]
	return float(second.split()[-1])


def get_yield_from_block(element, block, net_conversion = True):
	r"""
	Pulls the yield of the given element from the block read from the file.
	"""
	lines = block.split('\n')
	for line in lines:
		if line.split()[0] == element.lower():
			if net_conversion:
				return float(line.split()[-1])
			else:
				return float(line.split()[-2])
	raise ValueError("Yield not found for element: %s" % (element))


def convert_to_net(element, masslost, gross, z_initial):
	r"""
	Converts a gross yield into a net yield assuming a scaled solar
	composition.
	"""
	recycled = masslost * vice.solar_z[element] * (z_initial / 0.014)
	return gross - recycled # the net yield


def pull_yields_from_file(element, filename, z_initial, net_conversion = True):
	r"""
	Pulls all yields of the given element from a given file.
	"""
	yields = {}
	with open(filename, 'r') as file:
		while True:
			block = read_block(file)
			if block == "": break
			mass = get_mass_from_block(block)
			if mass in masses and mass not in yields.keys():
				yield_ = get_yield_from_block(element, block,
					net_conversion = net_conversion)
				if net_conversion: yield_ = convert_to_net(element,
					get_masslost_from_block(block), yield_, z_initial)
				yield_ /= mass
				yields[mass] = yield_
			else: pass
		file.close()
	return yields


def create_yield_file(element):
	r"""
	Creates the yield file in the parent directory for the specified element.
	"""
	with open("../%s.dat" % (element.lower()), 'w') as outfile:
		z0028_yields = pull_yields_from_file(element, files[0.0028], 0.0028,
			net_conversion = False)
		z007_yields = pull_yields_from_file(element, files[0.007], 0.007)
		z014_yields = pull_yields_from_file(element, files[0.014], 0.014)
		z03_yields = pull_yields_from_file(element, files[0.03], 0.03)
		for mass in masses:
			outfile.write("%g\t0.0028\t%.5e\n" % (mass, z0028_yields[mass]))
			outfile.write("%g\t0.007\t%.5e\n" % (mass, z007_yields[mass]))
			outfile.write("%g\t0.014\t%.5e\n" % (mass, z014_yields[mass]))
			outfile.write("%g\t0.03\t%.5e\n" % (mass, z03_yields[mass]))
		outfile.close()


if __name__ == "__main__": create_yield_file(sys.argv[1])

