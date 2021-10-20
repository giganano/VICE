# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from . import _output_utils
from ..pickles import pickled_object
import os
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
from ..dataframe._tracers cimport tracers as tracers_obj


def tracers(name):
	r"""
	Read in the star particles from a multizone simulation output.

	**Signature**: vice.stars(name)

	.. versionadded:: 1.2.0

	Parameters
	----------
	name : ``str``
		The full or relative path to the output directory. The '.vice'
		extension is not required.

	Returns
	-------
	stars : ``tracers`` [VICE ``dataframe`` derived class]
		A subclass of the VICE dataframe designed to store the star particles
		and to calculate relevant quantities automatically upon indexing.

	Raises
	------
	* IOError [Only occurs if the output has been altered]
		- Output directory not found.
		- Output files not formatted correctly.
		- Other VICE output files are missing from the output.

	.. seealso:: vice.core.dataframe.tracers

	Example Code
	------------
	>>> import vice
	>>> stars = vice.stars(example")
	>>> stars[100]
		vice.dataframe{
			formation_time -> 0.1
			zone_origin ----> 0.0
			zone_final -----> 0.0
			mass -----------> 29695920.0
			z(fe) ----------> 1.128362e-05
			z(sr) ----------> 6.203682e-10
			z(o) -----------> 0.0002587532
			[fe/h] ---------> -2.058141258363775
			[sr/h] ---------> -1.8831288138453521
			[o/h] ----------> -1.3445102993763647
			[sr/fe] --------> 0.17501244451842268
			[o/fe] ---------> 0.7136309589874101
			[o/sr] ---------> 0.5386185144689875
			z --------------> 0.0005393007991864363
			[m/h] ----------> -1.4142969718113587
			age ------------> 9.9
		}
	"""
	return c_tracers(name)


cdef tracers_obj c_tracers(name):
	"""
	Returns a tracers object for a given output.

	For details and documentation, see docstring of tracers function in this
	file.
	"""
	name = _output_utils._get_name(name)
	if _output_utils._is_multizone(name):
		zone0 = list(filter(lambda x: x.endswith(".vice"), os.listdir(name)))[0]
		adopted_solar_z = pickled_object.from_pickle(
			"%s/%s/attributes/Z_solar.obj" % (name, zone0)
		)
		return tracers_obj(filename = "%s/tracers.out" % (name),
			adopted_solar_z = adopted_solar_z
		)
	else:
		raise IOError("Not a multizone output: %s" % (name))

