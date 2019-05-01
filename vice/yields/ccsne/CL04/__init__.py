# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

"""
Chieffi & Limongi (2014), ApJ, 608, 405 Nucleosynthetic Yield Tools 
=================================================================== 
Importing this module will automatically set all yield settings 
from core collapse supernovae to the IMF-integrated yields as 
determined from the simulations ran by Chieffi & Limongi (2004) at 
Z = 0.02 ([M/H] = 0.15 if the solar abundance is Z = 0.014; Asplund 
et al. 2009). In doing so, it will default to an upper mass limit on star 
formation of 35 Msun. This is done to minimize numerical artifacts; this is 
the highest mass on the Chieffi & Limongi (2004) grid. 

VICE achieves this by calling yields.ccsne.fractional for every 
element built into the software and storing the returned value in 
yields.ccsne.settings.  

set_params :: Update the parameters with which the yields are calculated 

Notes 
===== 
By importing this module, the user does not sacrifice the flexibility of 
VICE's user specified yields. The fields of vice.yields.ccsne.settings can 
still be modified in whatever manner the user sees fit. 

This module is not imported with the simple 'import vice' statement. 

Example 
======= 
>>> from vice.yields.ccsne import CL04 
>>> CL04.set_params(lower = 0.3, upper = 40, IMF = "salpeter") 

References 
========== 
Asplund et al. (2009), ARA&A, 47, 481 
"""

from .. import settings as __settings 
from .. import fractional as __fractional 
from ....core._globals import _RECOGNIZED_ELEMENTS_ 

for i in range(len(_RECOGNIZED_ELEMENTS_)): 
	__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(_RECOGNIZED_ELEMENTS_[i], 
		study = "CL04", MoverH = 0.15, upper = 35)[0] 
del i 

def set_params(**kwargs): 
	"""
	Update the parameters with which the yields are calculated from the 
	Chieffi & Limongi (2004) data. 

	Parameters 
	========== 
	kwargs :: varying types 
		Keyword arguments to pass to yields.ccsne.fractional 

	Raises 
	====== 
	TypeError :: 
		::	The user has specified a keyword argument "study" 
	Other exceptions are raised by yields.ccsne.fractional 

	Example 
	======= 
	>>> from vice.yields.ccsne import CL04 
	>>> CL04.set_params(lower = 0.3, upper = 40, IMF = "salpeter") 

	References 
	========== 
	Chieffi & Limongi (2004), ApJ, 608, 405 
	"""
	if "study" in kwargs.keys(): 
		raise TypeError("set_params got an unexpected keyword argument: 'study'") 
	else: 
		if "MoverH" not in kwargs.keys(): 
			kwargs["MoverH"] = 0.15 
		else:
			pass 
		for i in range(len(_RECOGNIZED_ELEMENTS_)): 
			__settings[_RECOGNIZED_ELEMENTS_[i]] = __fractional(
				_RECOGNIZED_ELEMENTS_[i], study = "CL04", **kwargs)[0] 
		del i 

