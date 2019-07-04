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

_RECOGNIZED_STUDIES_ = ["seitenzahl13", "iwamoto99"] 

""" 
<--------------- C routine comment headers not duplicated here ---------------> 

Notes 
===== 
The following pythonic relative import line: 
from ...core cimport _ccsne 
produced the following line in the output .c file: 
#include "../src/objects.h" 
which appears in the _ccsne.pxd file. This renders a relative import from 
this file impossible, so we can simply cdef the necessary functions here. 
Since there is only one of them, this is simpler than modifying the 
vice/core/_ccsne.pxd file to allow it. 
""" 
cdef extern from "../../src/io.h": 
	double single_ia_mass_yield_lookup(char *file) 

#------------------------- SINGLE_IA_YIELD FUNCTION -------------------------# 
def single_detonation(element, study = "seitenzahl13", model = "N1"): 
	"""
	Lookup the mass yield in solar masses of a given element from a single 
	instance of a type Ia supernovae as determined by a given study and 
	explosion model. See section 5.2 of VICE's science documentation at 
	https://github.com/giganano/VICE/tree/master/docs for further details. 

	Signature: vice.yields.sneia.single(element, study = "seitenzahl13", 
		model = "N1") 

	Parameters 
	========== 
	element :: str [case-insensitive] 
		The symbol of the element to look up the yield for.  
	study :: str [case-insensitive] [default :: "seitenzahl13"] 
		A keyword denoting which study to adopt the yield from 
		Keyword and their Associated Studies
		------------------------------------ 
		"seitenzahl13" :: Seitenzahl et al. (2013), MNRAS, 429, 1156 
		"iwamoto99" :: Iwamoto et al. (1999), ApJ, 124, 439 
	model :: str [case-insensitive] [default :: N1] 
		A keyword denoting the model from the associated study to adopt. 

	Returns 
	======= 
	yield :: real number 
		The mass yield of the given element in solar masses as determined for 
		the specified model from the specified study. 

	Raises 
	====== 
	ValueError :: 
		::	The element is not built into VICE 
		::	The study is not built into VICE 
	LookupError :: 
		::	The study is recognized, but the model is not recognized for that 
			particular study 
	IOError :: [Occurs only if VICE's file structure has been tampered with] 
		::	The data file is not found. 

	Notes 
	===== 
	The only calculation performed by this function is a sum of the mass yields 
	of all isotopes of the given element reported by the study. Other than 
	that, it is a simple lookup function through the file tree built into 
	VICE. 

	Example 
	======= 
	>>> vice.single_ia_yield("fe") 
	    1.17390714 
	>>> vice.single_ia_yield("fe", study = "iwamoto99", model = "W70") 
	    0.77516 
	>>> vice.single_ia_yield("ni", model = "n100l") 
	    0.0391409000000526

	References 
	========== 
	Iwamoto et al. (1999), ApJ, 124, 439 
	Seitenzahl et al. (2013), MNRAS, 429, 1156 
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
		"seitenzahl13": 		"Seitenzahl et al. (2013), MNRAS, 429, 1156",  
		"iwamoto99": 			"Iwamoto et al. (1999), ApJ, 124, 439" 
	}

	# Models from their study keywords 
	recognized_models = {
		"seitenzahl13": 		["N1", "N3", "N5", "N10", "N40", "N100H", 
								"N100", "N100L", "N150", "N200", "N300C", 
								"N1600", "N100_Z0.5", "N100_Z0.1", "N100_Z0.01"], 
		"iwamoto99": 			["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", 
								"CDD2"] 
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
	"""
	Calculate an IMF-integrated fractional nucleosynthetic yield of a given 
	element from type Ia supernovae. Unlike vice.fractional_cc_yield, this 
	function does not require numerical quadrature. See section 5.2 of VICE's 
	science documentation at https://github.com/giganano/VICE/tree/master/docs 
	for futher details. 

	Signature: vice.yields.sneia.fractional(element, study = "seitenzahl13", 
		model = "N1", n = 2.2e-03) 

	Parameters 
	========== 
	element :: str [case-insensitive] 
		The symbol of the element to calculate the yield for. 
	study :: str [case-insensitive] [default :: "seitenzahl13"] 
		A keyword denoting which study to adopt single Ia yields from. 
		Keywords and their Associated Studies
		------------------------------------- 
		"seitenzahl13" :: Seitenzahl et al. (2013), MNRAS, 429, 1156 
		"iwamoto99" :: Iwamoto et al. (1999), ApJ, 124, 439 
	model :: str [case-insensitive] [default :: "N1"] 
		The model from the associated study to adopt. 
		Keywords and their Associated Models 
		------------------------------------
		"seitenzahl13" :: N1, N3, N5, N10, N40, N100H, N100, N100L, N150, 
			N200, N300C 
		"iwamoto99" :: W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2 
	n :: real number [default :: 2.2e-03] 
		The average number of type Ia supernovae produced per unit stellar 
		mass formed (N_ia/M_*). This parameter has units of Msun^{-1}. The 
		default value is derived from Maoz & Mannucci (2012), PASA, 29, 447. 

	Returns
	=======
	yield :: real number 
		The IMF-integrated yield. Unlike vice.fractional_cc_yield, there is 
		no associated numerical error with this function, because the 
		solution is analytic. 

	Raises
	======
	ValueError :: 
		:: 	The element is not built into VICE. 
		:: 	The study is not built into VICE. 
		::	n < 0  
	LookupError :: 
		:: The model is not recognized for the given study. 
	IOError :: [Occurs only if VICE's file structure has been tampered with] 
		:: 	The parameters passed to this function are allowed but the data 
			file is not found. 

	Notes
	=====
	This function evaluates the solution to the following equation: 
	
	y_x^Ia = (N_Ia/M_*)M_x

	where M_x is the value returned by vice.single_ia_yield. 

	Example 
	=======
	>>> vice.fractional_ia_yield("fe")
	    0.0025825957080000002
	>>> vice.fractional_ia_yield("ca") 
	    8.935489894764334e-06
	>>> vice.fractional_ia_yield("ni") 
	    0.00016576890932800003

	References 
	========== 
	Iwamoto et al. (1999), ApJ, 124, 439 
	Maoz & Mannucci (2012), PASA, 29, 447 
	Seitenzahl et al. (2013), MNRAS, 429, 1156 
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



