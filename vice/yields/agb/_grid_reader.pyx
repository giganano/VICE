# cython: language_level = 3, boundscheck = False
"""
This file wraps the C subroutines for reading AGB yield grids
"""

# Python imports
from __future__ import absolute_import
from ..._globals import _DIRECTORY_
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..._globals import _VERSION_ERROR_
from ...core.dataframe._builtin_dataframes import atomic_number
from ...core import _pyutils
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

# C imports
from libc.stdlib cimport malloc, free
from ._grid_reader cimport ELEMENT
from . cimport _grid_reader

_RECOGNIZED_STUDIES_ = tuple(["cristallo11", "karakas10", "ventura13",
	"karakas16"])
_VENTURA13_ELEMENTS_ = tuple(["he", "c", "n", "o", "ne", "na", "mg", "al", "si"])


#-------------------------- AGB_YIELD_GRID FUNCTION --------------------------#
def yield_grid(element, study = "cristallo11"):
	r"""
	Obtain the stellar mass-metallicity grid of fractional net yields from
	asymptotic giant branch stars published in a nucleosynthesis study.

	**Signature**: vice.yields.agb.grid(element, study = "cristallo11")

	Parameters
	----------
	element : ``str`` [case-insensitive]
		The symbol of the element to obtain the yield grid for.
	study : ``str`` [case-insensitive] [default : "cristallo11"]
		A keyword denoting which study to pull the yield table from.

		Recognized Keywords:

			- "cristallo11" : Cristallo et al. (2011, 2015) [1]_ [2]_
			- "karakas10" : Karakas (2010) [3]_
			- "ventura13" : Ventura et al. (2013) [4]_
			- "karakas16": Karakas & Lugaro (2016) [5]_; Karkas et al. (2018)
				[6]_

		.. versionadded:: 1.3.0
			The "ventura13" and "karakas16" yield models were introduced in
			version 1.3.0.

	Returns
	-------
	grid : ``tuple`` (2-D)
		A tuple of tuples containing the yield grid. The first axis is the
		stellar mass, and second is the metallicity
	masses : ``tuple``
		The masses in units of :math:`M_\odot` that the yield grid is sampled
		on.
	z : ``tuple``
		The metallicities by mass :math:`Z` that the yield grid is sample on.

	Raises
	------
	* ValueError
		- 	The study or the element are not built into VICE
	* LookupError
		- 	``study == "karakas10"`` and the atomic number of the element is
			:math:`\geq` 29. The Karakas (2010) study did not report yields
			for elements heavier the nickel.
		- 	The Ventura et al. (2013) tables include yields only for the
			following elements: he, c, n, o, ne, na, mg, al, si. A request for
			a table for any other element with raise an exception.
	* IOError [Occur's only if VICE's file structure has been modified]
		- 	The parameters passed to this function are allowed but the data
			file is not found.

	Notes
	-----
	The AGB star yields stored by VICE are reported *as published* by each
	corresponding study. With the exception of converting the values to
	*fractional* yields (i.e. by dividing by progenitor initial mass), they
	were not modified in any way.

	Example Code
	------------
	>>> y, m, z = vice.agb_yield_grid("sr")
	>>> m
	    (1.3, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0)
	>>> z
	    (0.0001, 0.0003, 0.001, 0.002, 0.003, 0.006, 0.008, 0.01, 0.014, 0.02)
	>>> # the fractional yield from 1.3 Msun stars at Z = 0.001
	>>> y[0][2]
	    2.32254e-09

	.. [1] Cristallo et al. (2011), ApJS, 197, 17
	.. [2] Cristallo et al. (2015), ApJS, 219, 40
	.. [3] Karakas (2010), MNRAS, 403, 1413
	.. [4] Ventura et al. (2013), MNRAS, 431, 3642
	.. [5] Kakaras & Lugaro (2016), ApJ, 825, 26
	.. [6] Karakas et al. (2018), MNRAS, 477, 421
	"""
	# Type checking
	if not isinstance(element, strcomp):
		raise TypeError("First argument must be of type string. Got: %s" % (
			type(element)))
	elif not isinstance(study, strcomp):
		raise TypeError("""Keyword arg 'study' must be of type string. \
Got: %s""" % (study))
	else:
		pass

	# Study keywords to their full citations
	studies = {
		"cristallo11": 			"Cristallo et al. (2011), ApJ, 197, 17",
		"karakas10": 			"Karakas (2010), MNRAS, 403, 1413",
		"ventura13": 			"Ventura et al. (2013), MNRAS, 431, 3642",
		"karakas16": 			"Karakas & Lugaro (2016), ApJ, 825, 26"
	}

	# Value checking
	if study.lower() not in _RECOGNIZED_STUDIES_:
		raise ValueError("Unrecognized study: %s" % (study))
	elif element.lower() not in _RECOGNIZED_ELEMENTS_:
		raise ValueError("Unrecognized element: %s" % (element))
	else:
		pass

	if study.lower() == "karakas10" and atomic_number[element.lower()] > 28:
		raise LookupError("""The %s study did not report yields for elements \
heavier than nickel (atomic number 28).""" % (studies["karakas10"]))
	elif (study.lower() == "ventura13" and
		element.lower() not in _VENTURA13_ELEMENTS_):
		raise LookupError("""The %s study did not report yields for the \
element %s. Only the following elements have tables available: %s.""" % (
			studies["ventura13"], element.lower(), str(_VENTURA13_ELEMENTS_)))
	else:
		pass

	# full path to the file containing the yield grid
	filename = find_yield_file(element, study)

	if not os.path.exists(filename):
		"""
		File not found ---> unless VICE was tampered with, this shouldn't
		happen.
		"""
		raise IOError("Yield file not found. Please re-install VICE.")
	else:
		pass

	cdef ELEMENT *e = _grid_reader.element_initialize()
	if _grid_reader.import_agb_grid(e, filename.encode("latin-1")):
		_grid_reader.element_free(e)
		raise SystemError("Internal Error: couldn't read yield file.")
	else:
		try:
			# copy over the yields, masses, and metallicities
			yields = e[0].agb_grid[0].interpolator[0].n_x_values * [None]
			for i in range(e[0].agb_grid[0].interpolator[0].n_x_values):
				yields[i] = e[0].agb_grid[0].interpolator[0].n_y_values * [0.]
				for j in range(e[0].agb_grid[0].interpolator[0].n_y_values):
					yields[i][j] = e[0].agb_grid[0].interpolator[0].zcoords[i][j]
			masses = [
				e[0].agb_grid[0].interpolator[0].xcoords[i] for i in range(
					e[0].agb_grid[0].interpolator[0].n_x_values)]
			metallicities = [
				e[0].agb_grid[0].interpolator[0].ycoords[i] for i in range(
					e[0].agb_grid[0].interpolator[0].n_y_values)]
		finally:
			_grid_reader.element_free(e)

		return [tuple(i) for i in [[tuple(j) for j in yields], masses,
			metallicities]]


def find_yield_file(element, study):
	"""
	Determines the full path to the file containing the mass-metallicity
	yield grid for a given element and study.

	Parameters
	==========
	element :: str [case-insensitive]
		The symbol for the element whose file is to be found
	study :: str [case-insensitive]
		The keyword for the study to lookup

	Returns
	=======
	path :: str
		The path to the yield file

	Raises
	======
	TypeError ::
		:: element is not of type str
		:: study is not of type str
	ValueError ::
		:: element is not recognized by VICE
		:: study is not recognized by VICE
	"""
	if not isinstance(element, strcomp):
		raise TypeError("Element must be of type str. Got: %s" % (
			type(element)))
	elif not isinstance(study, strcomp):
		raise TypeError("Study must be of type str. Got: %s" % (
			type(study)))
	elif element.lower() not in _RECOGNIZED_ELEMENTS_:
		raise ValueError("Unrecognized element: %s" % (element))
	elif study.lower() not in _RECOGNIZED_STUDIES_:
		raise ValueError("Unrecognized study: %s" % (study))
	else:
		return "%syields/agb/%s/%s.dat" % (_DIRECTORY_, study.lower(),
			element.lower())

