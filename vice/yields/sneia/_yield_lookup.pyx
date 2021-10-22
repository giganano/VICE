# cython: language_level = 3, boundscheck = False
"""
This file wraps the lookup functions for nuleosynthetic yields from SNe Ia.
"""

from __future__ import absolute_import
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..._globals import _DIRECTORY_
from ..._globals import _VERSION_ERROR_
import numbers
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()

_RECOGNIZED_STUDIES_ = ["seitenzahl13", "iwamoto99", "gronow21"]
from ._yield_lookup cimport single_ia_mass_yield_lookup


#------------------------- SINGLE_IA_YIELD FUNCTION -------------------------#
def single_detonation(element, study = "seitenzahl13", model = "N1"):
	
	r"""
	Lookup the mass yield of a given element from a single instance of a type
	Ia supernova (SN Ia) as determined by a specified study and explosion
	model.

	**Signature**: vice.yields.sneia.single(element, study = "seitenzahl13",
	model = "N1")

	Parameters
	----------
	element : ``str`` [case-insensitive]
		The symbol of the element to look up the yield for.
	study : ``str`` [case-insensitive] [default : "seitenzahl13"]
		A keyword denoting which study to adopt the yield from

		Keywords and their Associated Studies:

			- "seitenzahl13" : Seitenzahl et al. (2013) [1]_
			- "iwamoto99" : Iwamoto et al. (1999) [2]_
			- "gronow21" : Gronow et al. (2021a, b) [3]_ [4]_

	model : ``str`` [case-insensitive] [default : N1]
		A keyword denoting the explosion model from the associated study to
		adopt.

		Keywords and their Associated Models:

			- 	"seitenzahl13" : N1, N3, N5, N10, N20, N40, N100H, N100,
					N100L, N150, N200, N300C, N1600, N1600C, N100_Z0.5,
					N100_Z0.1, N100_Z0.01
			- 	"iwamoto99" : W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2
			- 	| "gronow21" : M08_03_001, M08_03_01, M08_03_1, M08_03_3,
				| 	M08_05_001, M08_05_01, M08_05_1, M08_05_3,
				| 	M08_10_001, M08_10_01, M08_10_1, M08_10_3,
				| 	M09_03_001, M09_03_01, M09_03_1, M09_03_3,
				| 	M09_05_001, M09_05_01, M09_05_1, M09_05_3,
				| 	M09_10_001, M09_10_01, M09_10_1, M09_10_3,
				| 	M10_02_001, M10_02_01, M10_02_1, M10_02_3,
				| 	M10_03_001, M10_03_01, M10_03_1, M10_03_3,
				| 	M10_05_001, M10_05_01, M10_05_1, M10_05_3,
				| 	M10_10_001, M10_10_01, M10_10_1, M10_10_3,
				| 	M11_05_001, M11_05_01, M11_05_1, M11_05_3

	Returns
	-------
	y : real number
		The mass yield of the given element in :math:`M_\odot` under the
		specified explosion model as reported by the nucleosynthesis study.

	Raises
	------
	* ValueError
		- 	The element is not built into VICE
		- 	The study is not built into VICE
	* LookupError
		- 	The study is recognized, but the model is not recognized for that
			particular study.
	* IOError [Occurs only if VICE's file structure has been modified]
		- 	The data file is not found.

	Notes
	-----
	The data stored in this module are reported for each corresponding study
	*as published*. The Seitenzahl et al. (2013) and Gronow et al. (2021a, b)
	models reported mass yields after complete decay of all radioactive
	nuclides with half-lives less than 2 Gyr, and the Iwamoto et al. (1999)
	study fully decayed *all* unstable isotopes; any additional treatment for
	radioactive isotopes is thus unnecessary.

	The Gronow et al. (2021a, b) models are named for the mass of the
	carbon-oxygen core, the mass of the helium shell, and the metallicity of
	the progenitor relative to solar, in that order.
	For example, the "M09_05_01" model refers to one with a 0.9 :math:`M_\odot`
	carbon-oxygen core and a 0.05 :math:`M_\odot` helium shell produced by a
	star that was initially at a metallicity of 0.1 :math:`Z_\odot`.

	Example Code
	------------
	>>> import vice
	>>> vice.yields.sneia.single("fe")
	1.17390714
	>>> vice.yields.sneia.single("fe", study = "iwamoto99", model = "W70")
	0.77516
	>>> vice.yields.sneia.single("fe", study = "iwamoto99", model = "CDD1")
	0.6479629999999998
	>>> vice.yields.sneia.single("ni", model = "n100l")
	0.0391409000000526
	>>> vice.yields.sneia.single("ni", model = "N150")
	0.0749891244
	>>> vice.yields.sneia.single("co", study = "gronow21", model = "M10_10_1")
	0.001058
	>>> vice.yields.sneia.single("co", study = "gronow21", model = "M09_05_001")
	0.0001572

	.. seealso::

		- vice.yields.sneia.fractional
		- vice.yields.sneia.gronow21
		- vice.yields.sneia.iwamoto99
		- vice.yields.sneia.seitenzahl13

	.. [1] Seitenzahl et al. (2013), MNRAS, 429, 1156
	.. [2] Iwamoto et al. (1999), ApJ, 124, 439
	.. [3] Gronow et al. (2021a), A&A, 649, 155
	.. [4] Gronow et al. (2021b), arxiv:2103.14050
	"""

	# Type check errors ---> element, study, and model must be of type string
	if not isinstance(element, strcomp):
		raise TypeError("First argument must be of type string. Got: %s" % (
			type(element)))
	elif not isinstance(study, strcomp):
		raise TypeError("Keyword arg 'study' must be of type string. Got: %s" % (
			type(study)))
	elif not isinstance(model, strcomp):
		raise TypeError("Keyword arg 'model' must be of type string. Got: %s" % (
			type(model)))
	else:
		pass


	# Full study citations from their keywords
	studies = {
		"seitenzahl13": "Seitenzahl et al. (2013), MNRAS, 429, 1156",
		"iwamoto99": 	"Iwamoto et al. (1999), ApJ, 124, 439",
		"gronow21": 	"""\
Gronow et al. (2021a, b), a:A&A, 649, 155, b:arxiv:2103.14050"""
	}

	# Models from their study keywords
	recognized_models = {
		"seitenzahl13": 	["N1", "N3", "N5", "N10", "N20", "N40", "N100H",
							"N100", "N100L", "N150", "N200", "N300C", "N1600",
							"N1600C", "N100_Z0.5", "N100_Z0.1", "N100_Z0.01"],
		"iwamoto99": 		["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1",
							"CDD2"],
		"gronow21": 		["M08_03_001", "M08_03_01", "M08_03_1", "M08_03_3",
							"M08_05_001", "M08_05_01", "M08_05_1", "M08_05_3",
							"M08_10_001", "M08_10_01", "M08_10_1", "M08_10_3",
							"M09_03_001", "M09_03_01", "M09_03_1", "M09_03_3",
							"M09_05_001", "M09_05_01", "M09_05_1", "M09_05_3",
							"M09_10_001", "M09_10_01", "M09_10_1", "M09_10_3",
							"M10_02_001", "M10_02_01", "M10_02_1", "M10_02_3",
							"M10_03_001", "M10_03_01", "M10_03_1", "M10_03_3",
							"M10_05_001", "M10_05_01", "M10_05_1", "M10_05_3",
							"M10_10_001", "M10_10_01", "M10_10_1", "M10_10_3",
							"M11_05_001", "M11_05_01", "M11_05_1", "M11_05_3"]
	}

	# Value check errors
	if element.lower() not in _RECOGNIZED_ELEMENTS_:
		raise ValueError("Unrecognized element: %s" % (element))
	elif study.lower() not in _RECOGNIZED_STUDIES_:
		raise ValueError("Unrecognized study: %s" % (study))
	elif model.upper() not in recognized_models[study.lower()]:
		raise LookupError("Model not recognized for the %s study: %s" % (
			studies[study.lower()], recognized_models[study.lower()]))
	else:
		pass

	# Get the full path to the yield file
	if '.' in model:
		# There are p's in place of .'s in the directory names
		model = model.replace('.', 'p')
	else:
		pass
	filename = "%syields/sneia/%s/%s/%s.dat" % (_DIRECTORY_, study.lower(),
		model.upper(), element.lower())
	if os.path.exists(filename):
		return single_ia_mass_yield_lookup(filename.encode("latin-1"))
	else:
		raise IOError("Yield file not found. Please re-install VICE.")


#----------------------- FRACTIONAL_IA_YIELD FUNCTION -----------------------#
def integrated_yield(element, study = "seitenzahl13", model = "N1",
	n = 2.2e-3):
	
	r"""
	Calculate a delay-time distribution integrated fractional nucleosynthetic
	yield of a given element from type Ia supernovae.

	**Signature**: vice.yields.sneia.fractional(element, study = "seitenzahl13",
	model = "N1", n = 2.2e-03)

	Parameters
	----------
	element : ``str`` [case-insensitive]
		The symbol of the element to calculate the yield for.
	study : ``str`` [case-sensitive] [default : "seitenzahl13"]
		A keyword denoting which study to adopt SN Ia mass yields from.

		Keywords and their Associated Studies:

			- "seitenzahl13" : Seitenzahl et al. (2013) [1]_
			- "iwamoto99" : Iwamoto et al. (1999), [2]_
			- "gronow21" : Gronow et al. (2021a, b) [3]_ [4]_

	model : ``str`` [case-insensitive] [default : "N1"]
		The model from the associated study to adopt.

		Keywords and their Associated Models:

			- 	"seitenzahl13" : N1, N3, N5, N10, N20, N40, N100H, N100,
					N100L, N150, N200, N300C, N1600, N1600C, N100_Z0.5,
					N100_Z0.1, N100_Z0.01
			- 	"iwamoto99" : W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2
			- 	| "gronow21" : M08_03_001, M08_03_01, M08_03_1, M08_03_3,
				| 	M08_05_001, M08_05_01, M08_05_1, M08_05_3,
				| 	M08_10_001, M08_10_01, M08_10_1, M08_10_3,
				| 	M09_03_001, M09_03_01, M09_03_1, M09_03_3,
				| 	M09_05_001, M09_05_01, M09_05_1, M09_05_3,
				| 	M09_10_001, M09_10_01, M09_10_1, M09_10_3,
				| 	M10_02_001, M10_02_01, M10_02_1, M10_02_3,
				| 	M10_03_001, M10_03_01, M10_03_1, M10_03_3,
				| 	M10_05_001, M10_05_01, M10_05_1, M10_05_3,
				| 	M10_10_001, M10_10_01, M10_10_1, M10_10_3,
				| 	M11_05_001, M11_05_01, M11_05_1, M11_05_3

	n : real number [default : 2.2e-03]
		The average number of type Ia supernovae produced per unit stellar
		mass formed :math:`N_\text{Ia}/M_\star` in :math:`M_\odot^{-1}`.

		.. note:: The default value for this parameter is adopted from
			Maoz & Mannucci (2012) [5]_.

	Returns
	-------
	y : real number
		The delay-time distribution integrated yield. This quantity represents
		the mass of some element produced over all SN Ia associated with a
		given stellar population in units of that stellar population's mass.
		This quantity is thus unitless (:math:`M_\odot` per :math:`M_\odot`).

	.. note:: Unlike vice.yields.ccsne.fractional, there is no associated
		numerical error with this function, because the solution is analytic.

	Raises
	------
	* ValueError
		- 	The element is not built into VICE.
		- 	The study is not built into VICE.
		- 	n < 0
	* LookupError
		- 	The model is not recognized for the given study.
	* IOError [Occurs only if VICE's file structure has been modified]
		- 	The parameters passed to this function are allowed but the data
			file is not found.

	Notes
	-----
	This function evaluates the solution to the following equation:

	.. math:: y_x^\text{Ia} = \left(\frac{N_\text{Ia}}{M_\star}\right)M_x

	where :math:`M_x` is the value returned by vice.yields.sneia.single, and
	:math:`N_\text{Ia}/M_\star` is specified by the parameter ``n``.

	The data stored in this module are reported for each corresponding study
	*as published*. The Seitenzahl et al. (2013) and Gronow et al. (2021a, b)
	models reported mass yields after complete decay of all radioactive
	nuclides with half-lives less than 2 Gyr, and the Iwamoto et al. (1999)
	study fully decayed *all* unstable isotopes; any additional treatment for
	radioactive isotopes is thus unnecessary.

	The Gronow et al. (2021a, b) models are named for the mass of the
	carbon-oxygen core, the mass of the helium shell, and the metallicity of
	the progenitor relative to solar, in that order.
	For example, the "M09_05_01" model refers to one with a 0.9 :math:`M_\odot`
	carbon-oxygen core and a 0.05 :math:`M_\odot` helium shell produced by a
	star that was initially at a metallicity of 0.1 :math:`Z_\odot`.

	Example Code
	------------
	>>> import vice
	>>> vice.yields.sneia.fractional("fe")
	0.0025825957080000002
	>>> vice.yields.sneia.fractional("fe", study = "iwamoto99", model = "W70")
	0.001705352
	>>> vice.yields.sneia.fractional("fe", study = "iwamoto99", model = "CDD1")
	0.0014255185999999997
	>>> vice.yields.sneia.fractional("ni", model = "n100l")
	8.610998000011574e-05
	>>> vice.yields.sneia.fractional("ni", model = "N150")
	0.00016497607368
	>>> vice.yields.sneia.fractional("co", study = "gronow21",
		model = "M10_10_1")
	2.3276e-06
	>>> vice.yields.sneia.fractional("co", study = "gronow21",
		model = "M09_05_001")
	3.4584000000000003e-07

	.. seealso::

		- vice.yields.sneia.single
		- vice.yields.sneia.gronow21
		- vice.yields.sneia.iwamoto99
		- vice.yields.sneia.seitenzahl13

	.. [1] Seitenzahl et al. (2013), MNRAS, 429, 1156
	.. [2] Iwamoto et al. (1999), ApJ, 124, 439
	.. [3] Gronow et al. (2021a), A&A, 649, 155
	.. [4] Gronow et al. (2021b), arxiv:2103.14050
	.. [5] Maoz & Mannucci (2012), PASA, 29, 447
	"""

	# n must be a non-negative real number
	if isinstance(n, numbers.Number):
		if n >= 0:
			# Type checking handled in single_detonation
			return n * single_detonation(element, study = study,
				model = model)
		else:
			raise ValueError("Keyword arg 'n' must be non-negative.")
	else:
		raise TypeError("Keyword arg 'n' must be a real number.")

