"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This file handles the integration of nucleosynthetic yields from SNe Ia 
"""

from __future__ import absolute_import
from ...core._globals import _RECOGNIZED_ELEMENTS
from ...core._globals import _DIRECTORY
from ...core._globals import _version_error
PATH = "%sdata/_sneia_yields/" % (_DIRECTORY)
import numbers 
import sys 
import os

if sys.version_info[0] == 2: 
	strcomp = basestring 
elif sys.version_info[0] == 3: 
	strcomp = str 
else:
	_version_error()

_RECOGNIZED_STUDIES_ = ["seitenzahl13", "iwamoto99"]





#-------------------------- SINGLE_IA_YIELD FUNCTION --------------------------# 
def single_detonation(element, study = "Seitenzahl13", model = "N1"):
	"""
	Calculates the mass in solar masses of a given element produced by a single 
	instance of a type Ia supernova from the results of previous theoretical 
	studies. 

	Args:
	=====
	element:		The elemental symbol

	Kwargs:
	=======
	study = "seitenzahl13":		The name of the study to pull yields from
	model = "W7":			The name of the model from the study

	Studies and their keywords:
	===========================
	Iwamoto99:				Iwamoto et al. (1999), ApJ, 124, 439
		Associated Models:		W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2
	Seitenzahl13: 				Seitenzahl et al. (2013), MNRAS, 429, 1156
		Associated Models: 		N1, N3, N5, N10, N20, N40, N100H, N100, N100L, 
								N150, N200, N300C, N1600, N100_Z0.5, N100_Z0.1, 
								N100_Z0.01
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
	if element.lower() not in _RECOGNIZED_ELEMENTS: 
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
def integrated_yield(element, study = "Seitenzahl13", model = "N1", 
	n = 2.2e-3):
	"""
	Calculates the IMF-integrated SNe Ia yield for a given element given a 
	number of SNe Ia detonations per unit solar mass formed n = N_Ia/M_*.

	The reported yield is simple: the mass of the element formed on average 
	by one SN Ia multiplied by the number of SNe Ia per unit mass of stars 
	formed. It thus has the sample form: 

	y_Ia(x) = M_Ia(x) * n 

	where M_Ia(x) is the single detonation yield and n is the mass-metric 
	number of SNe Ia. This function defaults to n = 2.2 x 10^-3 Msun^-1 as 
	found by Maoz & Mannucci (2012), which was also employed by the 
	Andrews et al. (2017) and Weinberg et al. (2017) studies. 

	Args:
	=====
	element:			The elemental symbol

	Kwargs:
	=======
	study = "Iwamoto99":		The name of the study to pull yields from
	model = "W7":			The name of the model from the study
	n = 2.2e-3: 			The number of SNe Ia per unit stellar mass formed 
					in Msun^-1 

	Studies and their Keywords:
	===========================
	Iwamoto99:				Iwamoto et al. (1999), ApJ, 124, 439
		Associated Models:		W7, W70, WDD1, WDD2, WDD3, CDD1, CDD2
	Seitenzahl13: 			Seitenzahl et al. (2013), MNRAS, 429, 1156
		Associated Models: 		N1, N3, N5, N10, N20, N40, N100H, N100, N100L, 
						N150, N200, N300C, N1600, N100_Z0.5, N100_Z0.1, 
						N100_Z0.01

	References: 
	===========
	Andrews, Weinberg, Schoenrich, & Johnson (2017), ApJ, 835, 224 
	Maoz & Mannucci (2012), PASA, 29, 447 
	Weinberg, Andrews, & Freudenberg (2017), ApJ, 837, 183
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



