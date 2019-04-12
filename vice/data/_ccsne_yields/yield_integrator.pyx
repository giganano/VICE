"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This script wraps the numerical integration features over mass sampled tables 
of core collapse supernovae yields. 
"""

from __future__ import absolute_import, unicode_literals 
from ...core._globals import _DIRECTORY
from ...core._globals import _RECOGNIZED_ELEMENTS
from ...core._globals import _RECOGNIZED_IMFS
from ...core._globals import ScienceWarning
from ...core._globals import _version_error
from ...core._yields import atomic_number
PATH = "%sdata/_ccsne_yields/" % (_DIRECTORY)
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
	_version_error()

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
	Calculates an IMF-integrated core-collapse supernovae fractional yield for 
	the given element. As implemented in the integrator class, the value 
	reported represents the fraction of the mass of a stellar population 
	that is immediately converted into the given element. In the case of a 
	zero yield, the returned error will be NaN. This is also the value that 
	will be returned in the event that a study did not report yields for a 
	given element (which is taken as an indication that it did not make up a 
	significant portion of the nucleosynthetic products). 

	Args:
	=====
	element:		The elemental symbol (case-insensitive)

	Kwargs:
	=======
	study = "LC18":		The name of the study to pull yields from (see below)
	MoverH = 0:		The total metallicity of the model [M/H]
	rotation = 0:		The rotational velocity from the study in km/s
	IMF = "kroupa":		The IMF to use (either Kroupa or Salpeter)
				(case-insensitive)
	method = "simpson":	The desired method of quadrature 
				Can be either "simpson", "midpoint", "trapezoid", 
				or "euler" (case-insensitive)
	lower = 0.08:		The lower mass limit on star formation in units of 
				solar masses
	upper = 100:		The upper mass limit on star formation in units of 
				solar masses
	tolerance = 1e-3:	The maximum allowed fractional error on the yield
	Nmin = 64:		The minimum number of bins in quadrature
	Nmax = 2e8:		The maximum number of bins in quadrature
				(A safeguard against divergent solutions)

	Returns:
	========
	A two-element python list
	returned[0]:		The fractional yield itself
	returned[1]:		The estimated fractional error on the reported yield
				WARNING:	The reported error is a pure numerical error, 
						associated only with the numerical integration. It does 
						not quantify the error associated with the physical 
						model. 

	Studies, their Keywords, Rotational Velocities, and Metallicities:
	==================================================================
	LC18:		Limongi & Chieffi (2018), ApJS, 237, 13
		rotation:		0, 150, 300 
		MoverH:			-3, -2, -1, 0
	CL13:		Chieffi & Limongi (2013), ApJ, 764, 21
		rotation: 		0, 300 
		MoverH:			0
	CL04:		Chieffi & Limongi (2004), ApJ, 608, 405
		rotation:		0
		MoverH:			-inf, -4, -2, -1, -0.37, 0.15
	WW95:		Woosley & Weaver (1995), ApJ, 101, 181
		rotation: 		0 
		MoverH: 		-inf, -4, -2, -1, 0

	Details:
	========
	Mass yields are sampled at various initial zero-age main sequence masses for 
	various metallicities and rotational velocities. At intermediate masses, mass 
	yields are computed from linear interpolation between those sampled. The 
	fractional yield is calculated from: 

	y = \int_8^upper m_x dn/dm dm / \int_lower^upper m dn/dm dm

	where y is the fractional yield, m_x is the mass of the isotope ejected 
	to ISM in their model, and dn/dm is the IMF that is assumed.

	VICE models core-collapse supernovae as coming from stars above 8 Msun, 
	and therefore all elements are assumed to have a mass yield of 0 for 
	each isotope at 8 Msun.  
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
	if element.lower() not in _RECOGNIZED_ELEMENTS:
		# Element has to be recognized by VICE 
		raise ValueError("Unrecognized element: %s" % (element))
	elif study.upper() not in studies:
		# Yields need to be built in 
		raise ValueError("Unrecognized study: %s" % (study.upper()))
	elif not os.path.exists("%s%s/FeH%s" % (PATH, study.upper(), MoverHstr)):
		# The study had to have reported yields at that metallicity 
		message = "The %s study does not have yields for [M/H] = %s" % (
			studies[study.upper()], MoverHstr)
		raise ValueError(message)
	elif not os.path.exists("%s%s/FeH%s/v%d" % (PATH, study.upper(), MoverHstr, 
		rotation)):
		# The study had to have reported yields at this rotational velocity 
		message = "The %s study does not have yields for v = %d km/s and " % (
			study.upper(), rotation)
		message += "[M/H] = %s" % (MoverHstr)
		raise ValueError(message)
	elif tolerance < 0 or tolerance > 1:
		# Tolerance must be between 0 and 1 
		message = "Tolerance must be a floating point value between 0 and 1."
		raise ValueError(message)
	elif lower > upper: 
		# Upper mass limit has to be larger than lower mass limit 
		message = "Lower mass limit greater than upper mass limit." 
		raise ValueError(message)
	elif IMF.lower() not in _RECOGNIZED_IMFS:
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
		message = "The %s study assumed a fixed yield of nickel-56. " % (
			studies[study.upper()])
		message += "For this reason, we caution the user on their yields of "
		message += "iron peak elements."  
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

