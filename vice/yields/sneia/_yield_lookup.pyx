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

			- "seitenzahl13": Seitenzahl et al. (2013) [1]_ 
			- "iwamoto99": Iwamoto et al. (1999) [2]_ 

	model : ``str`` [case-insensitive] [default : N1] 
		A keyword denoting the explosion model from the associated study to 
		adopt. 

		Keywords and their Associated Models: 

			- 	"seitenzahl13" : N1, N3, N5, N10, N20, N40, N100H, N100, 
				N100L, N150, N200, N300C, N1600, N1600C, N100_Z0.5, N100_Z0.1, 
				N100_Z0.01 
			- 	"iwamoto99" : W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2 

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
	* IOError [Occurs only if VICE's file structure has been tampered with] 
		- 	The data file is not found. 

	Example Code 
	------------
	>>> import vice 
	>>> vice.yields.sneia.single("fe") 
		1.17390714 
	>>> vice.yields.sneia.single("fe", study = "iwamoto99", model = "W70") 
		0.77516 
	>>> vice.yields.sneia.single("ni", model = "n100l") 
		0.0391409000000526

	.. seealso:: vice.yields.sneia.fractional 

	.. [1] Seitenzahl et al. (2013), MNRAS, 429, 1156 
	.. [2] Iwamoto et al. (1999), ApJ, 124, 439 
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
		"seitenzahl13": 		["N1", "N3", "N5", "N10", "N20", "N40", 
								"N100H", "N100", "N100L", "N150", "N200", 
								"N300C", "N1600", "N1600C", "N100_Z0.5", 
								"N100_Z0.1", "N100_Z0.01"], 
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
	
	r""" 
	Calculate an IMF-averaged fractional nucleosynthetic yield of a given 
	element from type Ia supernovae. 

	**Signature**: vice.yields.sneia.fractional(element, study = "seitenzahl13", 
	model = "N1", n = 2.2e-03) 

	Parameters 
	----------
	element : ``str`` [case-insensitive] 
		The symbol of the element to calculate the yield for. 
	study : ``str`` [case-sensitive] [default : "seitenzahl13"] 
		A keyword denoting which study to adopt SN Ia mass yields from. 

		Keywords and their Associated Studies: 

			- "seitenzahl13": Seitenzahl et al. (2013) [1]_ 
			- "iwamoto99": Iwamoto et al. (1999), [2]_ 

	model : ``str`` [case-insensitive] [default : "N1"] 
		The model from the associated study to adopt. 

		Keywords and their Associated Models: 

			- 	"seitenzahl13" : N1, N3, N5, N10, N20, N40, N100H, N100, 
				N100L, N150, N200, N300C, N1600, N1600C, N100_Z0.5, N100_Z0.1, 
				N100_Z0.01 
			- 	"iwamoto99" : W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2 

	n : real number [default : 2.2e-03] 
		The average number of type Ia supernovae produced per unit stellar 
		mass formed :math:`N_\text{Ia}/M_\star` in :math:`M_\odot^{-1}`. 

		.. note:: The default value for this parameter is adopted from 
			Maoz & Mannucci (2012) [3]_. 

	Returns 
	-------
	y : real number 
		The IMF-averaged yield. 

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
	* IOError [Occurs only if VICE's file structure has been tampered with] 
		- 	The parameters passed to this function are allowed but the data 
			file is not found. 

	Notes 
	-----
	This function evaluates the solution to the following equation: 

	.. math:: y_x^\text{Ia} = \left(\frac{N_\text{Ia}}{M_\star}\right)M_x 

	where :math:`M_x` is the value returned by vice.yields.sneia.single, and 
	:math:`N_\text{Ia}/M_\star` is specified by the parameter ``n``. 

	Example Code 
	------------
	>>> import vice 
	>>> vice.fractional_ia_yield("fe")
		0.0025825957080000002
	>>> vice.fractional_ia_yield("ca") 
		8.935489894764334e-06
	>>> vice.fractional_ia_yield("ni") 
		0.00016576890932800003

	.. [1] Seitenzahl et al. (2013), MNRAS, 429, 1156 
	.. [2] Iwamoto et al. (1999), ApJ, 124, 439 
	.. [3] Maoz & Mannucci (2012), PASA, 29, 447 
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

