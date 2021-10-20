"""
This file implements error handing for the CCSN yield functions in this
module
"""

from __future__ import absolute_import
__all__ = [
	"numeric_check",
	"string_check"
]
from ..._globals import _VERSION_ERROR_
from ..._globals import _DIRECTORY_
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	pass


# Recognized methods of numerical quadrature and yield studies
_RECOGNIZED_METHODS_ = tuple(["simpson", "midpoint", "trapezoid", "euler"])
_RECOGNIZED_STUDIES_ = tuple(["WW95", "LC18", "CL13", "CL04", "NKT13",
	"S16/W18", "S16/W18F", "S16/N20"])

# Keywords and their associated studies
_NAMES_ = {
	"LC18": 	"Limongi & Chieffi (2018), ApJS, 237, 13",
	"CL13": 	"Chieffi & Limongi (2013), ApJ, 764, 21 ",
	"NKT13": 	"Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457",
	"CL04": 	"Chieffi & Limongi (2004), ApJ, 608, 405",
	"WW95": 	"Woosley & Weaver (1995) ApJ, 101, 181",
	"S16/W18": 	"Sukhbold et al. (2016), ApJ, 821, 38 (W18 explosion engine)",
	"S16/W18F": "Sukhbold et al. (2016), ApJ, 821, 38 (W18 engine, forced)",
	"S16/N20": 	"Sukhbold et al. (2016), ApJ, 821, 38 (N20 explosion engine)"
}

# Keywords and their associated metallicities
_MOVERH_ = {
	"LC18": 		[-3, -2, -1, 0],
	"CL13": 		[0],
	"NKT13": 		[-float("inf"), -1.15, -0.54, -0.24, 0.15, 0.55],
	"CL04": 		[-float("inf"), -4, -2, -1, -0.37, 0.15],
	"WW95": 		[-float("inf"), -4, -2, -1, 0],
	"S16/W18": 		[0],
	"S16/W18F": 	[0],
	"S16/N20":		[0]
}

# Keywords and their associated rotational velocities
_ROTATION_ = {
	"LC18": 		[0, 150, 300],
	"CL13": 		[0, 300],
	"NKT13": 		[0],
	"CL04": 		[0],
	"WW95": 		[0],
	"S16/W18": 		[0],
	"S16/W18F": 	[0],
	"S16/N20":		[0]
}


def numeric_check(param, name):
	"""
	Ensures that a given parameter is a numerical value

	Parameters
	==========
	param :: object
		The parameter itself to type-check
	name :: str
		The name of the parameter as VICE sees it

	Raises
	======
	TypeError ::
		::	param is not a real number
	"""
	if not isinstance(param, numbers.Number):
		raise TypeError("Keyword arg '%s' must be a real number. Got: %s" % (
			name, type(param)))
	else:
		pass


def string_check(param, name):
	"""
	Ensures that a given parameter is a string

	Parameters
	==========
	param :: object
		The parameter itself to type-check
	name :: str
		The name of the parameter as VICE sees it

	Raises
	======
	TypeError ::
		::	params is not of type string
	"""
	if not isinstance(param, strcomp):
		raise TypeError("Keyword arg '%s' must be of type string. Got: %s" % (
			name, type(param)))
	else:
		pass


def find_yield_file(study, MoverH, rotation, which, element):
	"""
	Find the yield file associated with the given study, metallicity,
	rotational velocity, and element

	Parameters
	----------
	study : str [case-insensitive]
		The study to pull the yields from
	MoverH : real number
		The adopted metallicity
	rotation : real number
		The adopted rotational velocity in km/s
	which : str
		Either "wind" or "explosive", denoting which set of mass yields to
		take from.
	element : str [case-insensitive]
		The element to look up the yield for
	"""
	if MoverH % 1:
		MoverHstr = ("%.2f" % (MoverH)).replace('.', 'p')
	else:
		MoverHstr = "%d" % (int(MoverH))
	return "%syields/ccsne/%s/FeH%s/v%d/%s/%s.dat" % (
		_DIRECTORY_,
		study.upper(),
		MoverHstr,
		rotation,
		which,
		element.lower())

