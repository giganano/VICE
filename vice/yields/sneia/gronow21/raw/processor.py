r"""
This file reads in the files of raw data from Gronow et al. (2021a, 2021b) [1]_
[2]_.

.. [1] Gronow et al. (2021a), A&A, 649, 155
.. [2] Gronow et al. (2021b), A&A, arxiv:2103.14050
"""

import sys
import os

MODELS = {
	"table1.dat": ["M08_03_001", "M08_03_01", "M08_03_3"],
	"table2.dat": ["M08_05_001", "M08_05_01", "M08_05_3"],
	"table3.dat": ["M08_10_001", "M08_10_01", "M08_10_3"],
	"table4.dat": ["M09_03_001", "M09_03_01", "M09_03_3"],
	"table5.dat": ["M09_05_001", "M09_05_01", "M09_05_3"],
	"table6.dat": ["M09_10_001", "M09_10_01", "M09_10_3"],
	"table7.dat": ["M10_02_001", "M10_02_01", "M10_02_3"],
	"table8.dat": ["M10_03_001", "M10_03_01", "M10_03_3"],
	"table9.dat": ["M10_05_001", "M10_05_01", "M10_05_3"],
	"table10.dat": ["M10_10_001", "M10_10_01", "M10_10_3"],
	"table11.dat": ["M11_05_001", "M11_05_01", "M11_05_3"],
	"table23.dat": ["M08_10_1", "M08_05_1", "M08_03_1", "M09_10_1", "M09_05_1",
					"M09_03_1"],
	"table24.dat": ["M10_10_1", "M10_05_1", "M10_03_1", "M10_02_1", "M11_05_1"]
}


def make_output_dirs():
	r"""
	Creates the output directories for the yield files in the parent directory.
	"""
	os.chdir("..")
	for filename in MODELS.keys():
		for model in MODELS[filename]:
			os.system("mkdir %s" % (model))
	os.chdir("raw")


def remove_output_dirs():
	r"""
	Removes the output directories containing the yield files from the
	parent directory.
	"""
	os.chdir("..")
	for filename in MODELS.keys():
		for model in MODELS[filename]:
			os.system("rm -rf %s" % (model))
	os.chdir("raw")


def create_makefiles():
	r"""
	Creates the makefiles in the directories containing the yield files.
	"""
	os.chdir("..")
	for filename in MODELS.keys():
		for model in MODELS[filename]:
			with open("Makefile", "r") as srcmakefile:
				with open("./%s/Makefile" % (model), "w") as outmakefile:
					while True:
						line = srcmakefile.readline()
						if line == "": break
						if line.startswith("\t@ echo Cleaning"):
							outmakefile.write("%s%s/ \n" % (line[:-2], model))
						else:
							outmakefile.write(line)
					outmakefile.close()
				srcmakefile.close()
	os.chdir("raw")


def pull_yields(filename, model, element):
	assert model in MODELS[filename]
	idx = MODELS[filename].index(model)
	columns = [2 * idx + 1, 2 * idx + 2]
	yields = {}
	with open(filename, "r") as infile:
		while True:
			line = infile.readline()
			if line == "": break
			line = line.split()
			if line[0][2:].lower() == element:
				isotope = "%s%s" % (line[0][2:].lower(), line[0][:2])
				yields[isotope] = 0
				for i in columns: yields[isotope] += float(line[i])
			else: continue
		infile.close()
	return yields


def write_yields(infilename, model, element):
	yields = pull_yields(infilename, model, element)
	outfilename = "../%s/%s.dat" % (model, element)
	with open(outfilename, "w") as outfile:
		outfile.write("# isotope\tMass yield (Msun)\n")
		for isotope in yields.keys():
			outfile.write("%s\t%.4e\n" % (isotope, yields[isotope]))
		outfile.write("\n")
		outfile.close()


def main(element):
	for infilename in MODELS.keys():
		for model in MODELS[infilename]:
			write_yields(infilename, model, element.lower())


if __name__ == "__main__": main(sys.argv[1])



