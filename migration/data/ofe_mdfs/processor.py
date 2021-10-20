r"""
This script takes the files in the raw directory and combines the
|z| = 1.0 - 1.5 kpc bins with the |z| = 1.5 - 2.0 kpc bins, and simply copies
the rest to the current directory.
"""

import os

def combine_distributions(file1, file2, outfile):
	with open(file1, 'r') as in1:
		with open(file2, 'r') as in2:
			with open(outfile, 'w') as out:
				line1 = in1.readline()
				line2 = in2.readline()
				while line1 != "" and line2 != "":
					line1 = [float(_) for _ in line1.split()]
					line2 = [float(_) for _ in line2.split()]
					outline = line1[:]
					outline[-1] += line2[-1]
					for i in outline: out.write("%s\t" % (i))
					out.write("\n")
					line1 = in1.readline()
					line2 = in2.readline()
				out.close()
			in2.close()
		in1.close()


if __name__ == "__main__":
	rmin = [3, 5, 7, 9, 11]
	hmin = [0, 0.5, 1.0]
	FeHmin = [-0.4, -0.2, 0.0]
	for i in rmin:
		for j in hmin:
			for k in FeHmin:
				if j == 1.0:
					print("combining")
					combine_distributions(
						"./raw/Rmin%.1f_hmin%.1f_FeHmin%.1f.dat" % (i, j, k),
						"./raw/Rmin%.1f_hmin%.1f_FeHmin%.1f.dat" % (i, 1.5, k),
						"./Rmin%.1f_hmin%.1f_FeHmin%.1f.dat" % (i, j, k))
				else:
					os.system("cp ./raw/Rmin%.1f_hmin%.1f_FeHmin%.1f.dat ." % (
						i, j, k))

