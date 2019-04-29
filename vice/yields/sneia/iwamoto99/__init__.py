# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

"""
Iwamoto et al. (1999), ApJ, 124, 439 Nucleosynthetic Yield Tools 
================================================================ 
Importing this module will automatically set all yield settings 
from type Ia supernovae to the IMF-integrated yields as 
determined from the simulations ran by Iwamoto et al. (1999). It 
will default to the W70 explosion model.  

VICE achieves this by calling yields.sneia.fractional for 
every element built into the software and storing the returned value 
in yields.sneia.settings.  

set_params :: Update the parameters with which the yields are calculated. 

Notes 
===== 
By importing this module, the user does not sacrifice the flexibility of 
VICE's user-specified yields. After importing this module, the fields of 
vice.yields.sneia.settings can still be modified in whatever manner the 
user sees fit. 

This module is not imported with the simple 'import vice' statement. 

Example 
======= 
>>> from vice.yields.sneia import iwamoto99 
>>> iwamoto99.set_params(n = 1.5e-03) 
""" 

from .. import settings as __settings 
from .. import fractional as __fractional 
from ....core._globals import _RECOGNIZED_ELEMENTS_ 

for i in range(len(_RECOGNIZED_ELEMENTS_)): 
	__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(_RECOGNIZED_ELEMENTS_[i], 
		study = "iwamoto99", model = "W70") 
del i 

def set_params(**kwargs): 
	"""
	Update the parameters with which the yields are calculated from the 
	Iwamoto et al. (1999) data. 

	Parameters 
	========== 
	Kwargs :: varying types
		Keyword arguments to pass to yields.sneia.fractional. 

	Raises 
	====== 
	TypeError :: 
		::	The user has specified a keyword argument "study" 
	Other exceptions are raised by yields.sneia.fractional 

	See also 
	======== 
	yields.sneia.fractional docstring 

	Example 
	======= 
	>>> from vice.yields.sneia import iwamoto99 
	>>> iwamoto99.set_params(n = 1.5e-03) 

	References 
	========== 
	Iwamoto et al. (1999), ApJ, 124, 439 
	"""
	if "study" in kwargs.keys(): 
		raise TypeError("set_params got an unexpected keyword argument 'study'") 
	else: 
		if "model" not in kwargs.keys(): 
			kwargs["model"] = "W70" # Default to W70 unless told otherwise 
		else:
			pass 
		for i in range(len(_RECOGNIZED_ELEMENTS_)): 
			__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(
				_RECOGNIZED_ELEMENTS_[i], study = "iwamoto99", **kwargs) 
		del i 



