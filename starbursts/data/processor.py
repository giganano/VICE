"""
This file processes the Kirby et al. (2010) data from the raw ascii data table
into a processed output file where only stars with the entire multi-element
abundance is known.
"""

if __name__ == "__main__":
	with open("kirby2010processed.dat", 'w') as out:
		out.write("# dSph\tName\tRAJ200 (h:m:s)\tDEJ200 (d:m:s)\tVmag\tImag\t")
		out.write("Teff\tlogg\t[Fe/H]\terr([Fe/H])\t[Mg/Fe]\terr([Mg/Fe])\t")
		out.write("[Si/Fe]\terr([Si/Fe])\t[Ca/Fe]\terr([Ca/Fe])\t[Ti/Fe]\t")
		out.write("err([Ti/Fe])\n")
		with open("kirby2010.dat", 'r') as in_:
			for i in range(73):
				line = in_.readline()
			while line != "":
				if len(line.split()) == 22: out.write(line)
				line = in_.readline()
			in_.close()
		out.close()


