# cython: language_level = 3, boundscheck = False
"""
This file implements the history function, which returns a fromfile object
from a singlezone output.
"""

from __future__ import absolute_import
from . import _output_utils
from ..dataframe._fromfile cimport fromfile as fromfile_obj


def mdf(name):
	r"""
	Obtain a ``fromfile`` object from a VICE output containing the metallicity
	distribution function of stars.

	**Signature**: vice.mdf(name)

	Parameters
	----------
	name : ``str``
		The full or relative path to the output directory. The '.vice'
		extension is not required.

	Returns
	-------
	mdf : ``fromfile`` [VICE ``dataframe`` derived class]
		A subclass of the VICE dataframe designed to handle simulation output.

	Raises
	------
	* IOError [Only occurs if the output has been altered]
		- The output file is not found.
		- The output file is not formatted correctly.
		- Other VICE output files are missing from the output.

	Notes
	-----
	VICE normalizes metallicity distribution functions to a probability
	density, meaning that the area under the distribution is always equal to
	one. The value of the distribution in some bin times that bin's width
	denotes the fraction of stars with metallicities in that bin.

	.. note:: For abundances [X/H] and abundance ratios [X/Y] that in the
		simulation never achieve a value in the user-specified binspace, the
		distribution will be ``NaN`` in all bins.

	.. note:: For an output under a given name, the metallicity distribution
		function is stored in an ascii text file under name.vice/mdf.out. This
		allows users to open these files without VICE if necessary.

	.. seealso:: vice.core.dataframe.fromfile

	Example Code
	------------
	>>> import vice
	>>> example = vice.mdf("example")
	>>> example.keys()
		[“dn/d[sr/h],”,
		“dn/d[sr/fe],”
		“bin_edge_left,”
		“dn/d[o/h],”
		“dn/d[o/fe],”
		“dn/d[fe/h],”
		“bin_edge_right,”
		“dn/d[o/sr]”]
	>>> example["bin_edge_left"][:10]
		[-3.0, -2.95, -2.9, -2.85, -2.8, -2.75, -2.7, -2.65, -2.6, -2.55]
	>>> example[60]
		vice.dataframe{
			bin_edge_left --> 0.0
			bin_edge_right -> 0.05
			dn/d[fe/h] -----> 0.0
			dn/d[sr/h] -----> 0.0
			dn/d[o/h] ------> 0.0
			dn/d[sr/fe] ----> 0.06001488
			dn/d[o/fe] -----> 0.4337209
			dn/d[o/sr] -----> 0.0
		}
	"""
	return c_mdf(name)



cdef fromfile_obj c_mdf(name):
	"""
	Returns a fromfile object for the MDF of a given output.

	For details and documentation, see docstring of mdf function in this
	file.
	"""
	name = _output_utils._get_name(name)
	_output_utils._check_singlezone_output(name)
	with open("%s/mdf.out" % (name), 'r') as f:
		line = f.readline()
		keys = [i.lower() for i in line.split()[1:]]
		f.close()
	return fromfile_obj(
		filename = "%s/mdf.out" % (name),
		labels = keys
	)

