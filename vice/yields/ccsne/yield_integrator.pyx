"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This script wraps the numerical integration features over mass sampled tables 
of core collapse supernovae yields. 
"""

from __future__ import absolute_import, unicode_literals 
from ...core._globals import _DIRECTORY_
from ...core._globals import _RECOGNIZED_ELEMENTS_
from ...core._globals import _RECOGNIZED_IMFS_
from ...core._globals import ScienceWarning
from ...core._globals import _VERSION_ERROR_
from ...core._dataframes import atomic_number
PATH = "%syields/ccsne/" % (_DIRECTORY_)
from libc.stdlib cimport free
import warnings
import numbers
import math as m
import sys
import os

if sys.version_info[0] == 2: 
	strcomp = basestring 
elif sys.version_info[0] == 3: 
	strcomp = str
else:
	_VERSION_ERROR_()

# Recognzied methods of numerical quadrature 
_RECOGNIZED_METHODS_ = tuple(["simpson", "midpoint", "trapezoid", "euler"])




"""
<--------------- C routine comment headers not duplicated here --------------->

Conventionally these would be declared in a .pxd file and imported, but this 
is simpler when there are only two of them. 
"""
cdef extern from "../../src/cc_yields.h":
	double *numerator(char *file, char *IMF, double lower, double upper, 
		double tolerance, char *method, long Nmax, long Nmin)
	double *denominator(char *IMF, double lower, double upper, 
		double tolerance, char *method, long Nmax, long Nmin)






#----------------------- FRACTIONAL_CC_YIELD FUNCTION -----------------------#
def integrate(element, study = "LC18", MoverH = 0, rotation = 0, 
	IMF = "kroupa", method = "simpson", lower = 0.08, upper = 100, 
	tolerance = 1e-3, Nmin = 64, Nmax = 2e8):
	"""
	Calculates an IMF-integrated fractional nucleosynthetic yield of a given 
	element from core-collapse supernovae. VICE has built-in functions which 
	implement Gaussian quadrature to evaluate these integrals numerically. 
	See section 5.2 of VICE's science documentation at http://github.com/gigana
	no/VICE/tree/master/docs for further details. 

	Signature: vice.yields.ccsne.fractional(
		element, 
		study = "LC18", 
		MoverH = 0, 
		rotation = 0, 
		IMF = "kroupa", 
		method = "simpson", 
		lower = 0.08, 
		upper = 100, 
		tolerance = 1.0e-03, 
		Nmin = 64, 
		Nmax = 2.0e+08
	)

	Parameters
	========== 
	element :: str 
		The symbol of the element to calculate the IMF-integrated fractional 
		yield for. 
	study :: str [case-insensitive] [default :: "LC18"]
		A keyword denoting which study to adopt the yield from 
		Keywords and their Associated Studies
		-------------------------------------
		"LC18" :: Limongi & Chieffi (2018), ApJS, 237, 13
		"CL13" :: Chieffi & Limongi (2013), ApJ, 764, 21 
		"CL04" :: Chieffi & Limongi (2004), ApJ, 608, 405 
		"WW95" :: Woosley & Weaver (1995) ApJ, 101, 181 
	MoverH :: real number [default :: 0] 
		The total metallicity [M/H] of the exploding stars. There are only a 
		handful of metallicities recognized by each study, and VICE will 
		raise a LookupError if this value is not one of them. 
		Keywords and their Associated Metallicities
		-------------------------------------------
		"LC18" :: [M/H] = -3, -2, -1, 0 
		"CL13" :: [M/H] = 0 
		"CL04" :: [M/H] = -inf, -4, -2, -1, -0.37, 0.15 
		"WW95" :: [M/H] = -inf, -4, -2, -1, 0
	rotation :: real number [default :: 0] 
		The rotational velocity of the exploding stars in km/s. There are only 
		a handful of rotational velocities recognized by each study, and 
		VICE will raise a LookupError if this value is not one of them. 
		Keywords and their Associated Rotational Velocities
		---------------------------------------------------
		"LC18" :: v = 0, 150, 300 
		"CL13" :: v = 0, 300 
		"CL04" :: v = 0 
		"WW95" :: v = 0 
	IMF :: str [case-insensitive] [default :: "kroupa"] 
		The stellar initial mass function (IMF) to adopt. This must be either 
		"kroupa" (1) or "salpeter" (2). 
	method :: str [case-insensitive] [default :: "simpson"] 
		The method of quadrature. The numerical rules implemented here are of 
		the forms outlined in chapter 4 of Numerical Recipes (Press, Teukolsky, 
		Vetterling & Flannery). 
		Recognized Methods
		------------------ 
		"simpson"  
		"trapezoid" 
		"midpoint" 
		"euler" 
	lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses. 
	upper :: real number [default :: 100] 
		The upper mass limit on star formation in solar masses. 
	tolerance :: real number [default :: 0.001] 
		The numerical tolerance. The subroutines implementing Gaussian 
		quadrature in VICE will not return a result until the fractional 
		change between two successive integrations is smaller than this value. 
	Nmin :: real number [default :: 64] 
		The minimum number of bins in quadrature. 
	Nmax :: real number [default :: 2e+08] 
		The maximum number of bins in quadrature. Included as a failsafe 
		against solutions that don't converge numerically. 

	Returns 
	======= 
	yield :: real number 
		The numerically determined solution. 
	error :: real number 
		The estimated fractional numerical error. 

	Raises
	======
	ValueError :: 
		:: 	The element is not built into VICE 
		:: 	The study is not built into VICE 
		:: 	The tolerance is not between 0 and 1 
		:: 	lower > upper 
		::	The IMF is not built into VICE 
		:: 	The method of quadrature is not built into VICE 
		:: 	Nmin > Nmax 
	LookupError :: 
		:: 	The study did not report yields at the specified metallicity 
		:: 	The study did not report yields at the specified rotational
			velocity 
	ScienceWarning :: 
		:: 	upper is larger than the largest mass on the grid reported by the 
			specified study. VICE extrapolates to high masses in this case. 
		:: 	study is either "CL04" or "CL13" and the atomic number of the 
			element is between 24 and 28 (inclusive). VICE warns against 
			adopting these yields for iron peak elements. 
		:: 	Numerical quadrature did not converge within the maximum number 
			of allowed quadrature bins to within the specified tolerance. 

	Notes
	=====
	This function evaluates the solution to the following equation under the 
	assumption that all stars above 8 solar masses and below the upper mass 
	limit on star formation explode as a core-collapse supernova. 

	y_x^CC = \\frac{
		\\int_8^u M_x\\frac{dN}{dM}dM
	}{
		\\int_l^u M\\frac{dN}{dM}dM
	}

	where M_x is the mass of the element x produced in the super of a star 
	with initial mass M, and dN/dM is the stellar IMF. 

	Example
	=======
	>>> y, err = vice.fractional_cc_yield("o")
	>>> y
	    0.005643252355030168
	>>> err 
	    4.137197161389483e-06
	>>> y, err = vice.fractional_cc_yield("mg", study = "CL13") 
	>>> y 
	    0.000496663271667762 

	References
	==========
	(1) Kroupa (2001), MNRAS, 322, 231 
	Press, Teukolsky, Vetterling & Flannery, Numerical Recipes, (2007), 
		Cambridge University Press 
	(2) Salpeter (1955), ApJ, 121, 161 
	"""

	# The study keywords and their full citations
	studies = {
		"LC18":		"Limongi & Chieffi (2018), ApJS, 237, 18", 
		"CL13":		"Chieffi & Limongi (2013), ApJ, 764, 21", 
		"CL04":		"Chieffi & Limongi (2004), ApJ, 608, 405", 
		"WW95": 	"Woosley & Weaver (1995), ApJ, 101, 181"
	}

	# Type checking errors
	__string_check(study, 'study')		# study must be a string 
	if isinstance(MoverH, numbers.Number):
		"""
		Metallicity must be a number ---> get the subdirectory name 
		
		Within data/_ccsne_yields/ there are files for each study, and 
		within those files for each metallicity [M/H] rounded to two 
		decimal places with a 'p' in place of the decimal point. For 
		example, yields from stars with metallicities of [M/H] = 0.15 are 
		stored in a subdirectory 0p15/
		"""
		if MoverH % 1 == 0:
			MoverHstr = "%d" % (MoverH)
		else:
			MoverHstr = ("%.2f" % (MoverH)).replace('.', 'p')
	else:
		message = "Specified [M/H] must be a floating point value."
		raise TypeError(message)
	if not isinstance(rotation, numbers.Number):
		"""
		Within the directory for each metallicity is a directory for each 
		rotational velocity 
		"""
		message = "Keyword Arg 'rotation' must be a floating point value."
		raise TypeError(message)
	else:
		pass
	__string_check(IMF, 'IMF')			# IMF must be a string 
	__string_check(method, 'method')	# method must be a string 
	if not isinstance(lower, numbers.Number):
		# Lower stellar mass limit must be a number 
		message = "Keyword Arg 'lower' must be a floating point value."
		raise TypeError(message)
	else:
		pass
	if not isinstance(upper, numbers.Number):
		# Upper stellar mass limit must be a number 
		message = "Keyword Arg 'upper' must be a floating point value."
		raise TypeError(message)
	else:
		pass
	if not isinstance(tolerance, numbers.Number):
		# Tolerance must be a number 
		message = "Keyword Arg 'tolerance' must be a floating point value."
		raise TypeError(message)
	else:
		pass
	if not isinstance(Nmin, numbers.Number):
		# Minimum number of quadrature bins must be a number 
		message = "Keyword Arg 'Nmin' must be a floating point value."
		raise TypeError(message)
	else:
		pass
	if not isinstance(Nmax, numbers.Number):
		# Maximum number of quadrature bins must be a number 
		message = "Keyword Arg 'Nmax' must be a floating point value."
		raise TypeError(message)
	else:
		pass

	# Value checking errors
	if element.lower() not in _RECOGNIZED_ELEMENTS_:
		# Element has to be recognized by VICE 
		raise ValueError("Unrecognized element: %s" % (element))
	elif study.upper() not in studies:
		# Yields need to be built in 
		raise ValueError("Unrecognized study: %s" % (study.upper()))
	elif not os.path.exists("%s%s/FeH%s" % (PATH, study.upper(), MoverHstr)):
		# The study had to have reported yields at that metallicity 
		message = "The %s study does not have yields for [M/H] = %s" % (
			studies[study.upper()], MoverHstr)
		raise LookupError(message)
	elif not os.path.exists("%s%s/FeH%s/v%d" % (PATH, study.upper(), MoverHstr, 
		rotation)):
		# The study had to have reported yields at this rotational velocity 
		message = "The %s study does not have yields for v = %d km/s and " % (
			study.upper(), rotation)
		message += "[M/H] = %s" % (MoverHstr)
		raise LookupError(message)
	elif tolerance < 0 or tolerance > 1:
		# Tolerance must be between 0 and 1 
		message = "Tolerance must be a floating point value between 0 and 1."
		raise ValueError(message)
	elif lower > upper: 
		# Upper mass limit has to be larger than lower mass limit 
		message = "Lower mass limit greater than upper mass limit." 
		raise ValueError(message)
	elif IMF.lower() not in _RECOGNIZED_IMFS_:
		# IMF must be recognized by the software 
		raise ValueError("Unrecognized IMF: %s" % (IMF))
	elif method.lower() not in _RECOGNIZED_METHODS_:
		# Method of integration must be built into the quadrature functions 
		raise ValueError("Unrecognized method of quadrature: %s" % (method))
	elif Nmin > Nmax: 
		# Maximum number of bins must be larger than the minimum 
		message = "Minimum number of bins in quadrature must be smaller than "
		message += "maximum number of bins." 
		raise ValueError(message)

	"""
	Science Warnings 
	================
	1) The Limongi & Chieffi (2018) and Chieffi & Limongi (2013) studies 
	reported yields up to 120 Msun, so warn the user that for upper mass 
	limits higher than this that their yields will be extrapolated. The same 
	is true for the Chieffi & Limongi (2004) yields with upper mass limits 
	of 35 Msun. 

	2) The Chieffi & Limongi (2004) and the Chieffi & Limongi (2013) studies 
	involved numerical simulations of core collapse explosions with dialed-in 
	explosion energy. In their models, the mass of nickel-56 produced was 
	fixed. As such, one should exercise caution when employing their yields of 
	iron-peak elements. 

	3) The Woosley & Weaver (1995) study reported yields up to 40 Msun. Warn 
	the user about extrapolation to higher initial masses. 
	"""
	if study.upper() in ["LC18", "CL13"] and upper > 120:
		message = "Supernovae yields from the %s study are sampled on a grid " % (
			studies[study.upper()]) 
		message += "of stellar masses up to 120 Msun. Employing an upper mass "
		message += "limit larger than this may introduce numerical artifacts. "
		message += "Got: %g" % (upper) 
		warnings.warn(message, ScienceWarning)
	elif study.upper() == "CL04" and upper > 35: 
		message = "Supernovae yields from the %s study are only sampled up to " % (
			studies["CL04"])
		message += "35 Msun. With an upper mass limit of %g, linear " % (upper)
		message += "extrapolation of the yields may introduce numerical " 
		message += "artifacts." 
		warnings.warn(message, ScienceWarning)
	elif study.upper() == "WW95" and upper > 40: 
		message = "Supernovae yields from the %s study are sampled on a grid " % (
			studies["WW95"])
		message += "of stellar masses up to 40 Msun. Employing an upper mass " 
		message += "limit larger than this may introduce numerical artifacts. " 
		warnings.warn(message, ScienceWarning)
	else:
		pass 

	if ( study.upper() in ["CL04", "CL13"] and 
		24 <= atomic_number[element.lower()] <= 28 ): 
		message = "The %s study published only the results which adopted" % (
			studies[study.upper()]) 
		message += "a fixed yield of nickel-56, and these are the yields which "
		message += "are included in VICE. For this reason, we caution the user " 
		message += "on their yields of iron peak elements." 
		warnings.warn(message, ScienceWarning)
	else:
		pass


	# Find the file, but first check if the element comes from CCSNe

	"""
	VICE has included yields for every element, so they can be calculcated 
	no matter the dominant contributing factors. 
	"""
	filename = "%s%s/FeH%s/v%d/%s.dat" % (PATH, study.upper(), MoverHstr, 
		rotation, element.lower()) 
	if os.path.exists(filename): 
		pass 
	else: 
		"""
		If the file doesn't exist, the study didn't report yields for that 
		element (unless the user hacked their version of VICE). In this 
		case, that study would suggest that this element is not produced in 
		significant amounts by CCSNe, so we can safely return 0. 
		"""
		return [0, float("nan")]

	# Encode the strings 
	filename = filename.encode("latin-1")
	method = method.lower().encode("latin-1")
	IMF = IMF.lower().encode("latin-1")

	# Call the quadrature functions 
	cdef double *num = numerator(filename, IMF, lower, 
		upper, tolerance, method, long(Nmax), long(Nmin))
	cdef double *den = denominator(IMF, lower, upper, 
		tolerance, method, long (Nmax), long (Nmin))

	if num[1] > tolerance: 
		# If the numerator didn't converge 
		message = "Yield-weighted IMF integration did not converge. "
		message += "Estimated fractional error: %.2e" % (num[1]) 
		warnings.warn(message, ScienceWarning)
	else:
		pass
	if den[1] > tolerance: 
		# If the denominator didn't converge 
		message = "Mass-weighted IMF integration did not converge. "
		message += "Estimated fractional error: %.2e" % (den[1]) 
		warnings.warn(message, ScienceWarning)
	else:
		pass

	"""
	Determine the fractional yield and the associated numerical error, then 
	free up the memory and return the results 
	"""
	y = num[0] / den[0]
	errnum = num[1] * num[0]
	errden = den[1] * den[0]
	err = m.sqrt(errnum**2 / den[0]**2 + num[0]**2/den[0]**4 * errden**2)
	free(num)
	free(den)
	return [y, err]





#------------------------- TYPE CHECKING SUBROUTINE -------------------------# 
def __string_check(param, name):
	"""
	Determines if the passed parameter is of type string, and throws a 
	TypeError if it isn't. It also takes in the name for the purposes of 
	printing an error message. 
	"""
	if not isinstance(param, strcomp): 
		message = "Keyword Arg '%s' must be of type string. Got: %s" % (
			name, type(param))
		raise TypeError(message) 
	else:
		pass

