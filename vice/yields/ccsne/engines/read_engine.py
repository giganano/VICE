r"""
This file implements the function which reads an explodability engine from its
file.
"""

from __future__ import absolute_import
from ...._globals import _VERSION_ERROR_
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


def read(filename):
	r"""
	Reads in a file containing explodability engine data.

	Parameters
	----------
	filename : ``str``
		The name of the file to read in.

	Returns
	-------
	columns : ``list`` [elements of type ``list``]
		A 2-dimensional list containing the columns of the data file.
		``columns[0]`` will be the zero'th column, ``columns[1]`` the first,
		``columns[2]`` the second, and so on.

	If reading the engines from Sukhbold et al. (2016) [1]_, the return value
	will have two columns - progenitor zero age main sequence (ZAMS) masses and
	explosion frequencies. If reading the Ertl et al. (2016) [2]_ data, it
	will have three columns - progenitor ZAMS masses, :math:`M_4`, and
	:math:`\mu_4` values.

	Raises
	------
	* IOError
		- The file is not found.

	.. [1] Sukhbold et al. (2016), ApJ, 821, 38
	.. [2] Ertl et al. (2016), ApJ, 818, 124
	"""
	if isinstance(filename, strcomp):
		if os.path.exists(filename):
			contents = []
			with open(filename, 'r') as f:
				while True:
					line = f.readline()
					if line[0] != '#': break
				while line != "":
					contents.append([float(i) for i in line.split()])
					line = f.readline()
				f.close()
			columns = []
			for i in range(len(contents[0])):
				columns.append([row[i] for row in contents])
			return columns
		else:
			raise IOError("File not found: %s" % (filename))
	else:
		raise TypeError("Must be of type str. Got: %s" % (type(filename)))


