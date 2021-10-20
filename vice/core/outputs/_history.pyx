# cython: language_level = 3, boundscheck = False
"""
This file implements the history function, which returns a history object
from a singlezone output.
"""

from __future__ import absolute_import
from . import _output_utils
from ..pickles import pickled_object
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
from ..dataframe._history cimport history as history_obj
from . cimport _history


def history(name):
	r"""
	Obtain a ``history`` object from a VICE output containing the
	time-evolution of the interstellar medium and its relevant abundance
	information.

	**Signature**: vice.history(name)

	Parameters
	----------
	name : ``str``
		The full or relative path to the output directory. The '.vice'
		extension is not required.

	Returns
	-------
	hist : ``history`` [VICE ``dataframe`` derived class]
		A subclass of the VICE dataframe designed to store the output and to
		calculate relevant quantities automatically upon indexing.

	Raises
	------
	* IOError [Only occurs if the output has been altered]
		- Output directory not found.
		- Output files not formatted correctly.
		- Other VICE output files are missing from the output.

	.. seealso:: vice.core.dataframe.history

	Example Code
	------------
	>>> import numpy as np
	>>> import vice
	>>> vice.singlezone(name = "example").run(np.linspace(0, 10, 1001))
	>>> example = vice.history("example")
	>>> example["time"][:10]
		[0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
	>>> example["[o/fe]"][:10]
		[-0.30581989611140603,
		 -0.3059028126227887,
		 -0.3059856206579771,
		 -0.3060683202832149,
		 -0.30615091156463625,
		 -0.30623330628476564,
		 -0.30631559283107557,
		 -0.3063978595147838,
		 -0.30647984166504416,
		 -0.3065618040838354]
	>>> example[100]
		vice.dataframe{
			time -----------> 1.0
			mgas -----------> 5795119000.0
			mstar ----------> 2001106000.0
			sfr ------------> 2.897559
			ifr ------------> 9.1
			ofr ------------> 7.243899
			eta_0 ----------> 2.5
			r_eff ----------> 0.3534769
			z_in(fe) -------> 0.0
			z_in(sr) -------> 0.0
			z_in(o) --------> 0.0
			z_out(fe) ------> 0.0002769056
			z_out(sr) ------> 3.700754e-09
			z_out(o) -------> 0.001404602
			mass(fe) -------> 1604701.0
			mass(sr) -------> 21.44631
			mass(o) --------> 8139837.0
			z(fe) ----------> 0.0002769056166059748
			z(sr) ----------> 3.700754031107903e-09
			z(o) -----------> 0.0014046022178319376
			[fe/h] ---------> -0.6682579454664828
			[sr/h] ---------> -1.1074881208001155
			[o/h] ----------> -0.6098426789720387
			[sr/fe] --------> -0.43923017533363273
			[o/fe] ---------> 0.05841526649444406
			[o/sr] ---------> 0.4976454418280768
			z --------------> 0.0033582028978416337
			[m/h] ----------> -0.6200211036287412
			lookback -------> 9.0
		}
	"""
	return c_history(name)



cdef history_obj c_history(name):
	"""
	Returns a history object for a given output.

	For details and documentation, see docstring of history function in this
	file.
	"""
	name = _output_utils._get_name(name)
	_output_utils._check_singlezone_output(name)
	adopted_solar_z = pickled_object.from_pickle(
		"%s/attributes/Z_solar.obj" % (name)
	)
	return history_obj(
		filename = "%s/history.out" % (name),
		adopted_solar_z = adopted_solar_z
	)


