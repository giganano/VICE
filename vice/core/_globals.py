"""
This file, included with the VICE package, is protected under the terms of the 
associated MIT License, and any use or redistribution of this file in original 
or altered form is subject to the copyright terms therein. 

This file scripts the settings for the user's simulations which should be 
independent of the galaxy evolution parameters that they build in. We 
discourage the user from modifying any of the source code of these 
structures for use within VICE. 
"""

import warnings
import numbers
import inspect
import pickle
try: 
	# Allows functions to be written to config files and stored as defaults 
	import dill
except ImportError:
	pass
import sys
import os

__all__ = ["_DEFAULT_FUNC_", "_DEFAULT_BINS_", "_RECOGNIZED_ELEMENTS_", 
	"_RECOGNIZED_IMFS_", "ScienceWarning"] 
__all__ = [str(i) for i in __all__] # appease python 2 strings 

# The path to the directory after installation 
_DIRECTORY_ = os.path.dirname(os.path.abspath(__file__))
_DIRECTORY_ = _DIRECTORY_[:-4] # removes 'core' to get full path to dir

"""
The default bins into which a stellar metallicity distribution function 
will be sorted by the singlezone class. It spans the range from -3 to 1 in each 
[X/H] abundance and [X/Y] abundance ratio with 0.01-dex width bins. 
"""
_DEFAULT_BINS_ = 81 * [0.]
for i in range(81): 
	_DEFAULT_BINS_[i] = -3. + 0.05 * i 

"""
Elements and initial mass functions built into VICE. The user cannot simply 
modify these fields and have new elements or IMFs built into the software. As 
such, we do not recommend the user modify these attributes. 
"""
_RECOGNIZED_ELEMENTS_ = tuple(["c", "n", "o", "f", "ne", "na", 
	"mg", "al", "si", "p", "s", "cl", "ar", "k", "ca", "sc", "ti", "v", "cr", 
	"mn", "fe", "co", "ni", "cu", "zn", "ga", "ge", "as", "se", "br", "kr", 
	"rb", "sr", "y", "zr", "nb", "mo", "ru", "rh", "pd", "ag", "cd", "in", 
	"sn", "sb", "te", "i", "xe", "cs", "ba", "la", "ce", "pr", "nd", "sm", 
	"eu", "gd", "tb", "dy", "ho", "er", "tm", "yb", "lu", "hf", "ta", "w", 
	"re", "os", "ir", "pt", "au", "hg", "tl", "pb", "bi"])
_RECOGNIZED_IMFS_ = tuple(["kroupa", "salpeter"])


def _DEFAULT_FUNC_(t):
	"""
	The default function for an singlezone object. This function takes time as 
	an argument and always returns the value of 9.1. By default, 
	singlezone runs in infall mode, meaning that this corresponds to an 
	infall rate of 9.1 Msun yr^-1 at all times. 
	"""
	return 9.1

def _VERSION_ERROR_():
	"""
	Raises a RuntimeError in the event that the user has import VICE into a 
	python interpreter that is not version 2.7 or >= 3.5. This is included as 
	a failsafe against errors related to unsupported python interpreters. 
	"""
	message = "Only python version 2.7 and >= 3.5 are supported by VICE" 
	raise RuntimeError(message)	

class ScienceWarning(UserWarning): 
	"""
	A custom warning class designed to treat as a distinct set of warnings 
	those related to the scientific accuracy or precision of values returned 
	from any given function. Although it is not recommended, users can silence 
	this specific class of warnings via: 

		>>> warnings.filterwarnings("ignore", categore = vice.ScienceWarning) 

	Alternatively, they may silence all warnings within VICE via: 

		>>> vice.warnings.filterwarnings("ignore") 

	To silence all warnings globally: 

		>>> warnings.filterwarnings("ignore") 
	"""
	pass 


