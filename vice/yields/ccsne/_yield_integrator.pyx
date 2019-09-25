# cython: language_level = 3, boundscheck = False
""" 
This script wraps the numerical integration features over mass sampled 
tables of core collapse supernovae yields. 
""" 

from __future__ import absolute_import 
from ..._globals import _DIRECTORY_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _RECOGNIZED_IMFS_ 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import ScienceWarning 
from ...core._builtin_dataframes import atomic_number 
from ...core import _pyutils 
import math as m 
import warnings 
import numbers 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

# C Functions 
from libc.stdlib cimport malloc, free 
""" 
<--------------- C routine comment headers not duplicated here ---------------> 

Notes 
===== 
The following pythonic relative import line: 
from ...core cimport _ccsne 
produced the following line in the output .c file: 
#include "..src/objects.h" 
which appears in the _ccsne.pxd file. This renders a relative import from 
this file impossible, so we can simply cdef the necessary functions here. 
Since there are only two of them, this is simpler than modifying the 
vice/core/_ccsne.pxd file to allow it. 
""" 
cdef extern from "../../src/objects.h": 
	ctypedef struct IMF_: 
		char *spec 
		double m_lower 
		double m_upper 
		double *mass_distribution 

	ctypedef struct INTEGRAL: 
		double (*func)(double) 
		double a 
		double b 
		double tolerance 
		unsigned long method 
		unsigned long Nmax 
		unsigned long Nmin 
		unsigned long iters 
		double result 
		double error 

cdef extern from "../../src/quadrature.h": 
	INTEGRAL *integral_initialize() 
	void integral_free(INTEGRAL *intgrl) 

cdef extern from "../../src/ccsne.h": 
	void set_explodability_criteria(double *masses, unsigned int n_masses, 
		double *explodability)
	# unsigned short IMFintegrated_fractional_yield_numerator(INTEGRAL *intgrl, 
	# 	char *file, char *IMF) 
	# unsigned short IMFintegrated_fractional_yield_denominator(INTEGRAL *intgrl, 
	# 	char *IMF)  
	unsigned short IMFintegrated_fractional_yield_numerator(INTEGRAL *intgrl, 
		IMF_ *imf, char *file) 
	unsigned short IMFintegrated_fractional_yield_denominator(INTEGRAL *intgrl, 
		IMF_ *imf)  

cdef extern from "../../src/imf.h": 
	unsigned long SPEC_CHARP_SIZE 
	double IMF_STEPSIZE 
	IMF_ *imf_initialize(double m_lower, double m_upper) 
	void imf_free(IMF_ *imf) 
	unsigned long n_mass_bins(IMF_ imf) 
	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 

cdef extern from "../../src/utils.h": 
	void set_char_p_value(char *dest, int *ords, int length)

cdef double *copy_pylist(source): 
	""" 
	Copy a python list into a C double. This is in vice/core/_cutils.pxd, but 
	a relative import of that file is not possible; see notes above. 
	""" 
	cdef double *arr = <double *> malloc (len(source) * sizeof(double)) 
	for i in range(len(source)): 
		arr[i] = source[i] 
	return arr 

cdef IMF_ *imf_object(IMF, m_lower, m_upper): 
	if callable(IMF): 
		_pyutils.args(IMF, """Stellar IMF must accept only one numerical \
parameter.""") 
		spec = "custom" 
	elif isinstance(IMF, strcomp): 
		if IMF.lower() in _RECOGNIZED_IMFS_: 
			spec = IMF.lower() 
		else: 
			raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	else: 
		raise TypeError("""Keyword arg 'IMF' must be either a string denoting \
a built-in IMF or a callable function denoting a custom IMF. Got: %s""" % (
			type(IMF))) 
	# cdef char *cspec = <char *> malloc (1 + len(spec) * sizeof(char)) 
	cdef IMF_ *imf = imf_initialize(m_lower, m_upper) 
	cdef int *ords = <int *> malloc (len(spec) * sizeof(char)) 
	for i in range(len(spec)): 
		ords[i] = ord(spec[i]) 
	set_char_p_value(imf[0].spec, ords, len(spec)) 
	free(ords) 

	cdef double *mapped 
	if callable(IMF): 
		masses = _pyutils.range_(m_lower, m_upper, IMF_STEPSIZE) 
		mapped = <double *> malloc (len(masses) * sizeof(double)) 
		for i in range(len(masses)): 
			mapped[i] = IMF(masses[i]) 
		x = imf_set_mass_distribution(imf, mapped) 
		free(mapped) 
		if x: 
			imf_free(imf) 
			raise ArithmeticError("""Custom IMF evaluated to negative, inf, \
or nan for at least one stellar mass.""") 
		else: 
			pass 
	else: 
		pass 
	
	return imf 



# Recognized methods of numerical quadrature and yield studies 
_RECOGNIZED_METHODS_ = tuple(["simpson", "midpoint", "trapezoid", "euler"]) 
_RECOGNIZED_STUDIES_ = tuple(["WW95", "LC18", "CL13", "CL04", "NKT13"])  

#----------------------- FRACTIONAL_CC_YIELD FUNCTION -----------------------# 
def integrate(element, study = "LC18", MoverH = 0, rotation = 0, 
	mass_ranges = [], explodability = [], IMF = "kroupa", method = "simpson", 
	m_lower = 0.08, m_upper = 100, tolerance = 1e-3, Nmin = 64, Nmax = 2e8): 
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
		m_lower = 0.08, 
		m_upper = 100, 
		tolerance = 1.0e-03, 
		Nmin = 64, 
		Nmax = 2.0e+08
	)

	Parameters
	========== 
	element :: str [case-insensitive] 
		The symbol of the element to calculate the IMF-integrated fractional 
		yield for. 
	study :: str [case-insensitive] [default :: "LC18"]
		A keyword denoting which study to adopt the yield from 
		Keywords and their Associated Studies
		-------------------------------------
		"LC18"	:: Limongi & Chieffi (2018), ApJS, 237, 13
		"CL13"	:: Chieffi & Limongi (2013), ApJ, 764, 21 
		"NKT13"	:: Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457
		"CL04"	:: Chieffi & Limongi (2004), ApJ, 608, 405 
		"WW95"	:: Woosley & Weaver (1995) ApJ, 101, 181 
	MoverH :: real number [default :: 0] 
		The total metallicity [M/H] of the exploding stars. There are only a 
		handful of metallicities recognized by each study, and VICE will 
		raise a LookupError if this value is not one of them. 
		Keywords and their Associated Metallicities
		-------------------------------------------
		"LC18"	:: [M/H] = -3, -2, -1, 0 
		"CL13"	:: [M/H] = 0 
		"NKT13"	:: [M/H] = -inf, -1.15, -0.54, -0.24, 0.15, 0.55 
		"CL04"	:: [M/H] = -inf, -4, -2, -1, -0.37, 0.15 
		"WW95"	:: [M/H] = -inf, -4, -2, -1, 0
	rotation :: real number [default :: 0] 
		The rotational velocity of the exploding stars in km/s. There are only 
		a handful of rotational velocities recognized by each study, and 
		VICE will raise a LookupError if this value is not one of them. 
		Keywords and their Associated Rotational Velocities
		---------------------------------------------------
		"LC18"	:: v = 0, 150, 300 
		"CL13"	:: v = 0, 300 
		"NKT13"	:: v = 0
		"CL04"	:: v = 0 
		"WW95"	:: v = 0 
	mass_ranges :: array-like [default :: empty list] 
		The first piece of information on stellar explodability criteria: mass 
		ranges of stars. The elements of this object must be 2-element 
		array-like objects whose elements are positive numerical values 
		denoting the lower and upper limits on stellar initial mass ranges. 
		By default, this function assumes that all stars explode. 
	explodability :: array-like [default :: empty list] 
		The second piece of information on stellar explodability criteria: the 
		fractions of stars that explode. The elements of this object are 
		matched component-wise to the elements of the keyword argument 
		'mass_ranges'. By default, this function assumes that all stars 
		explode. 
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
	m_lower :: real number [default :: 0.08] 
		The lower mass limit on star formation in solar masses. 
	m_upper :: real number [default :: 100] 
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
		:: 	m_lower > m_upper 
		::	The IMF is not built into VICE 
		:: 	The method of quadrature is not built into VICE 
		:: 	Nmin > Nmax 
		::	Stellar mass in mass_ranges is negative 
		:: 	Any combination of elements of mass_ranges overlap 
		:: 	Explodability fraction not between 0 and 1 
	LookupError :: 
		:: 	The study did not report yields at the specified metallicity 
		:: 	The study did not report yields at the specified rotational
			velocity 
	ScienceWarning :: 
		:: 	m_upper is larger than the largest mass on the grid reported by the 
			specified study. VICE extrapolates to high masses in this case. 
		:: 	study is either "CL04" or "CL13" and the atomic number of the 
			element is between 24 and 28 (inclusive). VICE warns against 
			adopting these yields for iron peak elements. 
		:: 	Numerical quadrature did not converge within the maximum number 
			of allowed quadrature bins to within the specified tolerance. 
		:: 	Explodability criteria above 25 Msun specified in combination with 
			the Limongi & Chieffi (2018) study. 

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

	Explodability criteria will be overspecified when calculating yields from 
	the Limongi & Chieffi (2018) study, in which stars above 25 Msun do not 
	explode. The yields they report at these masses are that which comes from 
	the wind. 

	Example
	=======
	>>> y, err = vice.yields.ccsne.fractional("o")
	>>> y
	    0.005643252355030168
	>>> err 
	    4.137197161389483e-06
	>>> y, err = vice.yields.ccsne.fractional("mg", study = "CL13") 
	>>> y 
	    0.000496663271667762 
	# Stars from 12-15, 20-30, and 40-100 Msun explode 10%% of the time. 
	>>> y, err = vice.yields.ccsne.fractional("mg", study = "CL13", 
		mass_ranges = [[12, 15], [20, 30], [40, 100]], 
		explodability = [0.1, 0.1, 0.1]) 
	>>> y 
		0.00039911211487501523 

	References
	==========
	(1) Kroupa (2001), MNRAS, 322, 231 
	Press, Teukolsky, Vetterling & Flannery, Numerical Recipes, (2007), 
		Cambridge University Press 
	(2) Salpeter (1955), ApJ, 121, 161 
	""" 

	# Type checking errors 
	if not isinstance(element, strcomp): 
		raise TypeError("First argument must be of type string. Got: %s" % ( 
			type(element))) 
	else: 
		__string_check(study, "study") 
		# __string_check(IMF, "IMF") error handling now in imf_object 
		__string_check(method, "method") 
		__numeric_check(MoverH, "MoverH") 
		__numeric_check(rotation, "rotation") 
		__numeric_check(m_lower, "m_lower") 
		__numeric_check(m_upper, "m_upper") 
		__numeric_check(tolerance, "tolerance") 
		__numeric_check(Nmin, "Nmin") 
		__numeric_check(Nmax, "Nmax") 


	""" 
	Mass ranges must be either an empty array-like object or a series of 
	2-element array-like objects containing numerical values. The explodability 
	criteria must then have a number between 0 and 1 for each of those mass 
	ranges. 
	""" 
	mass_ranges = _pyutils.copy_array_like_object(mass_ranges) 
	explodability = _pyutils.copy_array_like_object(explodability) 
	if len(explodability) == len(mass_ranges): 
		for i in explodability: 
			if not isinstance(i, numbers.Number): 
				raise ValueError("""Explodability fraction must be between 0 \
and 1. Got: %g""" % (i)) 
			else: 
				pass 
		for i in mass_ranges: 
			i = _pyutils.copy_array_like_object(i) 
			if len(i) == 2: 
				for j in i: 
					if not isinstance(j, numbers.Number): 
						raise TypeError("""Stellar mass for explodability \
prescription must be a numerical value. Got: %s""" % (type(j))) 
					elif j < 0: 
						raise ValueError("""Stellar mass for explodability \
prescription must be a non-negative. Got: %s""" % (type(j))) 
					else: 
						j = float(j) 
			else: 
				raise ValueError("""Stellar explodability mass ranges must be \
only 2-element array-like objects.""") 
	else: 
		raise ValueError("""Keyword arg 'explodability' must be of the same \
length as the keyword arg 'mass_range'. explodability length: %d; mass_ranges \
length: %d""" % (len(explodability), len(mass_ranges))) 

	# Study keywords and their full citations 
	studies = {
		"LC18":			"Limongi & Chieffi (2018), ApJS, 237, 18", 
		"CL13":			"Chieffi & Limongi (2013), ApJ, 764, 21", 
		"CL04":			"Chieffi & Limongi (2004), ApJ, 608, 405", 
		"WW95": 		"Woosley & Weaver (1995), ApJ, 101, 181", 
		"NKT13": 		"Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457" 
	} 

	# The name of the directory holding yield files at this metallicity 
	if MoverH % 1 == 0: 
		MoverHstr = "%d" % (MoverH) 
	else: 
		MoverHstr = ("%.2f" % (MoverH)).replace('.', 'p') 

	# Value checking errors 
	if element.lower() not in _RECOGNIZED_ELEMENTS_: 
		raise ValueError("Unrecognized element: %s" % (element)) 
	elif study.upper() not in _RECOGNIZED_STUDIES_: 
		raise ValueError("Unrecognized study: %s" % (study)) 
	elif not os.path.exists("%syields/ccsne/%s/FeH%s" % (_DIRECTORY_, 
		study.upper(), MoverHstr)): 
		raise LookupError("The %s study does not have yields for [M/H] = %s" % (
			studies[study.upper()], MoverHstr.replace('p', '.')))  
	elif not os.path.exists("%syields/ccsne/%s/FeH%s/v%d" % (_DIRECTORY_, 
		study.upper(), MoverHstr, rotation)): 
		raise LookupError("""The %s study did not report yields for v = %d \
km/s and [M/H] = %g""" % (study, rotation, MoverH)) 
	elif tolerance < 0 or tolerance > 1: 
		raise ValueError("Tolerance must be between 0 and 1.") 
	elif m_lower >= m_upper: 
		raise ValueError("Lower lass limit larger than upper mass limit.") 
	# elif IMF.lower() not in _RECOGNIZED_IMFS_: moved to imf_object function 
	# 	raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	elif method.lower() not in _RECOGNIZED_METHODS_: 
		raise ValueError("Unrecognized method of quadrature: %s" % (method)) 
	elif Nmin >= Nmax: 
		raise ValueError("""Minimum number of bins in quadrature must be \
smaller than maximum number of bins.""") 
	else: 
		pass 

	""" 
	Set the explosion criteria in C, after making sure that none of the mass 
	ranges overlap. 
	""" 
	if len(mass_ranges) > 0: 
		_masses = (2 * len(mass_ranges)) * [0.] 
		for i in range(len(mass_ranges)): 
			if 0 <= explodability[i] <= 1:
				for j in range(2): 
					_masses[2 * i + j] = mass_ranges[i][j] 
			else: 
				raise ValueError("""All explosion fractions must be between 0 \
and 1. Got: %g""" % (explodability[i]))
		# check for overlap (there's too much information to calculate a yield) 
		if _masses != sorted(_masses): 
			raise ValueError("Explodability mass ranges overlap.") 
		else: 
			pass 
		if _masses[-1] > 25 and study.upper() == "LC18": 
			warnings.warn("""CCSNe progenitors above an initial mass of 25 \
Msun did not explode in the %s study, and instead they report only the yields \
from the stellar winds. The explodability criteria are thus \
overspecified.""" % (studies[study.upper()]), ScienceWarning) 
		else: 
			pass 
	else: 
		_masses = [m_lower, m_upper] 
		explodability = [1] 

	# Send the explodability criteria to ccsne.c, the rest is handled there. 
	cdef double *c_masses = copy_pylist(_masses) 
	cdef double *c_explodability = copy_pylist(explodability) 
	set_explodability_criteria(c_masses, len(_masses), c_explodability) 
	free(c_masses) 
	free(c_explodability) 

	"""
	Science Warnings 
	================
	1) The Limongi & Chieffi (2018) and Chieffi & Limongi (2013) studies 
	reported yields up to 120 Msun, so warn the user that for upper mass 
	limits higher than this that their yields will be extrapolated. The same 
	is true for the Chieffi & Limongi (2004) yields with upper mass limits 
	of 35 Msun and the Woosley & Weaver (1995) study with upper mass limits 
	of 40 Msun. 

	2) The Chieffi & Limongi (2004) and the Chieffi & Limongi (2013) studies 
	involved numerical simulations of core collapse explosions with dialed-in 
	explosion energy. In their models, the mass of nickel-56 produced was 
	fixed. As such, one should exercise caution when employing their yields of 
	iron-peak elements. 

	3) The Woosley & Weaver (1995) study reported yields up to 40 Msun. Warn 
	the user about extrapolation to higher initial masses. 
	"""
	upper_mass_limits = {
		"LC18":		120, 
		"CL13": 	120, 
		"CL04": 	35, 
		"WW95": 	40, 
		"NKT13": 	300 if MoverH == -float("inf") else 40 
	} 

	if m_upper > upper_mass_limits[study.upper()]: 
		warnings.warn("""Supernovae yields from the %s study are sampled on a \
grid of stellar masses up to %d Msun at this metallicity. Employing an upper \
mass limit larger than this may introduce numerical artifacts. \
Got: %g Msun""" % (
		studies[study.upper()], upper_mass_limits[study.upper()], m_upper), 
		ScienceWarning) 
	else: 
		pass 

	if ( study.upper() in ["CL04", "CL13"] and 
		24 <= atomic_number[element.lower()] <= 28 ): 
		warnings.warn("""The %s study published only the results which \
adopted a fixed yield of nickel-56, and these are the yields which are 
installed in this version of VICE. For this reason, we caution the user on \
these yields of iron peak elements.""" % (studies[study.upper()]), 
			ScienceWarning) 
	else: 
		pass 

	"""
	VICE includes yields for every element that these studies reported. 
	However, if a study didn't report yields for a given element, that study 
	would suggest that the element is not produced in significant amounts by 
	CCSNe, so we can safely return a 0 and raise a ScienceWarning. 
	""" 
	filename = "%syields/ccsne/%s/FeH%s/v%d/%s.dat" % (_DIRECTORY_, 
		study.upper(), 
		MoverHstr, 
		rotation, 
		element.lower()) 
	if not os.path.exists(filename): 
		warnings.warn("""The %s study did not report yields for the element \
%s. If adopting these yields for simulation, it is likely that this yield \
can be approximated as zero at this metallicity. Users may exercise their \
own discretion by modifying their CCSNe yield settings directly.""" % (
			studies[study.upper()], element), ScienceWarning) 
		return [0, float("nan")] 
	else: 
		pass 

	print("a") 
	cdef IMF_ *imf_obj = imf_object(IMF, m_lower, m_upper) 
	print("b") 

	# Compute the yield 
	cdef INTEGRAL *num = integral_initialize() 
	print("c") 
	num[0].a = m_lower 
	print("d") 
	num[0].b = m_upper 
	print("e") 
	num[0].tolerance = tolerance 
	print("f") 
	num[0].method = <unsigned long> sum([ord(i) for i in method.lower()]) 
	print("g") 
	num[0].Nmax = <unsigned long> Nmax 
	print("h") 
	num[0].Nmin = <unsigned long> Nmin 
	print("i") 
	try: 
		x = IMFintegrated_fractional_yield_numerator(num, 
			# filename.encode("latin-1"), 
			# IMF.lower().encode("latin-1")) 
			imf_obj, 
			filename.encode("latin-1")) 
		print("j") 
		if x == 1: 
			warnings.warn("""Yield-weighted IMF integration did not converge. \
Estimated fractional error: %.2e""" % (num[0].error), ScienceWarning) 
		elif x: 
			raise SystemError("Internal Error") 
		else: 
			pass 
		print("k") 
	finally: 
		print("l") 
		numerator = [num[0].result, num[0].error, num[0].iters] 
		print("m") 
		integral_free(num) 
		print("n") 


	cdef INTEGRAL *den = integral_initialize() 
	den[0].a = m_lower 
	den[0].b = m_upper 
	den[0].tolerance = tolerance 
	den[0].method = <unsigned long> sum([ord(i) for i in method.lower()]) 
	den[0].Nmax = <unsigned long> Nmax 
	den[0].Nmin = <unsigned long> Nmin 
	try: 
		x = IMFintegrated_fractional_yield_denominator(den, 
			# IMF.lower().encode("latin-1")) 
			imf_obj) 
		if x == 1: 
			warnings.warn("""Mass-weighted IMF integration did not converge. \
Estimated fractional error: %.2e""" % (den[0].error), ScienceWarning) 
		elif x: 
			raise SystemError("Internal Error") 
		else: 
			pass 
	finally: 
		denominator = [den[0].result, den[0].error, den[0].iters] 
		integral_free(den) 
		imf_free(imf_obj) 

	y = numerator[0] / denominator[0] 
	errnum = numerator[1] * numerator[0] 
	errden = denominator[1] * denominator[0] 
	err = m.sqrt(errnum**2 / denominator[0]**2 + numerator[0]**2 / 
		denominator[0]**4 * errden**2) 

	return [y, err] 


#------------------------- TYPE CHECKING SUBROUTINES -------------------------# 
def __numeric_check(param, name): 
	if not isinstance(param, numbers.Number): 
		raise TypeError("Keyword arg '%g' must be a real number. Got: %s" % (
			name, type(param))) 
	else: 
		pass 


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

