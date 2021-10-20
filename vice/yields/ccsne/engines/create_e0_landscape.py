r"""
This file reads in the mu4_M4.dat file and constructs an explodability landscape
using the mu4 and M4 pre-SN valuesfrom S16 with the formalism from
Griffith et al. (2021)
"""

from __future__ import absolute_import
from ...._globals import _VERSION_ERROR_
import sys
import os
# import
import scipy.interpolate


if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


def read(filename):
	r"""
	Reads in a file containing mu4 M4 data for all stellar masses.

	Parameters
	----------
	filename : str
		The name of the file to read in.

	Returns
	-------
	MZAMS : list
		The masses on which the mu4 and M4 parameters are sampled.
	M4: list
		The mass value at s=4 for the pre-SN star
	mu4 : list
		The mu4 parameter for the pre-SN star. mu4M4 represents the mass
		derivative at s=4

	Raises
	------
	* IOError
		- The file is not found.
	"""
	if isinstance(filename, strcomp):
		if os.path.exists(filename):
			MZAMS = []
			M4 = []
			mu4 = []
			with open(filename, 'r') as f:
				f.readline()
				f.readline()
				line = f.readline()
				while line != "":
					line = [float(i) for i in line.split()]
					MZAMS.append(line[0])
					M4.append(line[1])
					mu4.append(line[2])
					line = f.readline()
				f.close()
			return [MZAMS, M4, mu4]
		else:
			raise IOError("File not found: %s" % (filename))
	else:
		raise TypeError("Must be of type str. Got: %s" % (type(filename)))


def e0_landscape(filename, e0, M):
	r"""
	Reads in the pre-SN stellar values and returns the explodability landscape
	assiciated the the specified e0.

	Parameters
	----------
	e0 : float
		The value of e0 to set the threshold of explodability
	M : float
		The ZAMS stellar mass whose explodability you want to evaluate


	Returns
	-------
	Explodability : float
		A value of 0 if the specified stellar mass explodes
		A value of 1 if the specified stellar mass collapses to a BH

	Raises
	------
	- error if e0 is not a float?
	"""

	M_ZAMS, M4s, mu4s = read(filename)

	interp_mu4 = scipy.interpolate.interp1d(M_ZAMS, mu4s)
	interp_M4 = scipy.interpolate.interp1d(M_ZAMS, M4s)

	mu4 = interp_mu4(M)
	M4 = interp_M4(M)

	e = 0.28*M4*mu4 - mu4 + e0

	if e<=0: return 0
	elif e>0: return 1

e = e0_landscape('mu4_M4.dat', 0.06, 20)
print(e)


