# cython: language_level=3, boundscheck=False
"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This file handles the integration of nucleosynthetic yields from SNe Ia 
"""

from __future__ import absolute_import
from ...core._globals import _RECOGNIZED_ELEMENTS_
from ...core._globals import _DIRECTORY_
from ...core._globals import _VERSION_ERROR_
PATH = "%syields/sneia/" % (_DIRECTORY_)
import numbers 
import sys 
import os

if sys.version_info[0] == 2: 
	strcomp = basestring 
elif sys.version_info[0] == 3: 
	strcomp = str 
else:
	_VERSION_ERROR_()

_RECOGNIZED_STUDIES_ = ["seitenzahl13", "iwamoto99"]





#-------------------------- SINGLE_IA_YIELD FUNCTION --------------------------# 
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
		message = "First argument must be of type string. Got: %s" % (
			type(element)) 
		raise TypeError(message) 
	elif not isinstance(study, strcomp): 
		message = "Keyword arg 'study' must be of type string. Got: %s" % (
			type(study)) 
		raise TypeError(message)
	elif not isinstance(model, strcomp): 
		message = "Keyword arg 'model' must be of type string. Got: %s" % (
			type(study))
		raise TypeError(message) 
	else:
		pass 

	# Value check errors 
	if element.lower() not in _RECOGNIZED_ELEMENTS_: 
		# The element has to be recognized 
		raise ValueError("Unrecognized element: %s" % (element))
	elif study.lower() not in _RECOGNIZED_STUDIES_: 
		# The study must be built into VICE 
		raise ValueError("Unrecognized study: %s" % (study)) 
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

	if model.upper() not in recognized_models[study.lower()]: 
		# If the study didn't use this model 
		message = "Model not recognized for the %s study: %s" % (
			studies[study.lower()], recognized_models[study.lower()]) 
		raise LookupError(message) 
	else:
		pass 

	# The full path to the yield file 
	if '.' in model: 
		# replace '.' with 'p' for lookup
		model = model.replace('.', 'p')
	else:
		pass
	yield_file = "%s%s/%s/%s.dat" % (PATH, study.lower(), model.upper(), 
		element.lower()) 
	if os.path.exists(yield_file): 
		y = 0. 
		with open(yield_file, 'r') as f: 
			# Open the file and read the first line 
			line = f.readline()  
			while line[0] == '#': 	# Read passed the header 
				line = f.readline() 
			while line != "": 
				if len(line.split()) == 2: 
					# Add the mass-yield of the isotope ---> second column 
					y += float(line.split()[1]) 
				else:
					pass 
				line = f.readline() 		# read the new line 
			# Close the file, return the yield, and call it a day 
			f.close() 
		return y
	else: 
		# The file wasn't found ---> reinstall VICE 
		message = "Yield file not found. Please re-install VICE." 
		raise IOError(message) 





#------------------------ FRACTIONAL_IA_YIELD FUNCTION ------------------------# 
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

	# n must be a number 
	if isinstance(n, numbers.Number): 
		# n must be non-negative 
		if n >= 0: 
			# Type-checking on other parameters handled in single_detonation
			return n * single_detonation(element, study = study, 
				model = model) 
		else: 
			# ValueError ---> n is negative 
			raise ValueError("Keyword arg n must be non-negative.") 
	# TypeError ---> n must be a numerical value 
	else: 
		raise TypeError("Keyword arg n must be a real number.") 



