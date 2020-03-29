"""
VICE global variables 
===================== 
This module contains variables that are global to the VICE package. 

Contents 
======== 
_DEFAULT_FUNC_ :: <function> 
	The default func attribute of the singlezone class. It takes in one 
	parameter and returns the value of 9.1 always. 
_DEFAULT_BINS_ :: list 
	The default bins attribute of the singlezone class. It is all values 
	between -3 and +1 (inclusive) in steps of 0.05. 
_RECOGNIZED_ELEMENTS_ :: tuple 
	The elements for which VICE is capable of simulating the enrichment and 
	calculating nucleosynthetic yields. This includes all astrophysically 
	produced elements between carbon and bismuth. 
_RECOGNIZED_IMFS_ :: tuple 
	The stellar initial mass functions built into VICE. Currently this 
	includes only the Kroupa (1) and Salpeter (2) IMFs. 

References 
========== 
(1) Kroupa (2001), MNRAS, 322, 231 
(2) Salpeter (1955), ApJ, 121, 161 
"""

__all__ = ["_DEFAULT_FUNC_", "_DEFAULT_BINS_", "_RECOGNIZED_ELEMENTS_", 
	"_RECOGNIZED_IMFS_"] 

import os


# The path to the directory after installation 
_DIRECTORY_ = "%s/" % (os.path.dirname(os.path.abspath(__file__)))

"""
The default bins into which a stellar metallicity distribution function 
will be sorted by the singlezone class. It spans the range from -3 to 1 in each 
[X/H] abundance and [X/Y] abundance ratio with 0.01-dex width bins. 
"""
_DEFAULT_BINS_ = [-3. + 0.05 * i for i in range(81)] 

"""
Elements and initial mass functions built into VICE. The user cannot simply 
modify these fields and have new elements or IMFs built into the software. As 
such, we do not recommend the user modify these attributes. 
"""
_RECOGNIZED_ELEMENTS_ = tuple(["he", "c", "n", "o", "f", "ne", "na", 
	"mg", "al", "si", "p", "s", "cl", "ar", "k", "ca", "sc", "ti", "v", "cr", 
	"mn", "fe", "co", "ni", "cu", "zn", "ga", "ge", "as", "se", "br", "kr", 
	"rb", "sr", "y", "zr", "nb", "mo", "ru", "rh", "pd", "ag", "cd", "in", 
	"sn", "sb", "te", "i", "xe", "cs", "ba", "la", "ce", "pr", "nd", "sm", 
	"eu", "gd", "tb", "dy", "ho", "er", "tm", "yb", "lu", "hf", "ta", "w", 
	"re", "os", "ir", "pt", "au", "hg", "tl", "pb", "bi"])
_RECOGNIZED_IMFS_ = tuple(["kroupa", "salpeter"]) 
_RECOGNIZED_RIAS_ = tuple(["plaw", "exp"]) 


def _DEFAULT_FUNC_(t):
	"""
	The default function for an singlezone object. This function takes time as 
	an argument and always returns the value of 9.1. By default, 
	singlezone runs in infall mode, meaning that this corresponds to an 
	infall rate of 9.1 Msun yr^-1 at all times. 
	"""
	return 9.1 


def _DEFAULT_TRACER_MIGRATION_(zone, tform): 
	""" 
	The default stellar migration prescription for multizone simulations. 
	This is a function of initial zone number and formation time for the 
	stellar population tracer particles, which returns a funtion of time. 
	This function then returns zone numbers for tracer particles that form 
	in that zone at that time. 

	By default, the tracer particles do not migrate between zones. That is, 
	the zone number for particles forming in zone n remain in zone n at all 
	times. 

	See Also 
	======== 
	multizone.migration.stars 
	""" 
	def _ZONE_OCCUPATION_(time): 
		""" 
		The zone number the tracer particle occupies is simply the one it 
		forms in. 
		""" 
		return zone 
	return _ZONE_OCCUPATION_ 


def _VERSION_ERROR_():
	"""
	Raises a RuntimeError in the event that the user has import VICE into a 
	python interpreter that is not version 2.7 or >= 3.5. This is included as 
	a failsafe against errors related to unsupported python interpreters. 
	"""
	message = "Only python version 2.7 and >= 3.5 are supported by VICE" 
	raise RuntimeError(message)	


class ScienceWarning(Warning): 
	"""
	A custom warning class designed to treat as a distinct set of warnings 
	those related to the scientific accuracy or precision of values returned 
	from any given function. Although it is not recommended, users can silence 
	this specific class of warnings via: 

		>>> warnings.filterwarnings("ignore", category = vice.ScienceWarning) 

	Alternatively, they may silence all warnings within VICE via: 

		>>> vice.warnings.filterwarnings("ignore") 

	To silence all warnings globally: 

		>>> warnings.filterwarnings("ignore") 
	"""
	pass 


class VisibleDeprecationWarning(Warning): 
	""" 
	A deprecation warning which - contrary to the python default deprecation 
	warning - is visible by default. Features which raise this warning are 
	deprecated and will be removed in a future release of VICE. 
	""" 
	pass 

