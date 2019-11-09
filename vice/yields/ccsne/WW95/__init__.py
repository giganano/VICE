"""
Woosley & Weaver (1995), ApJ, 101, 181 Nucleosynthetic Yield Tools 
================================================================== 
Importing this module will automatically set all yield settings 
from core collapse supernovae to the IMF-integrated yields as 
determined from the simulations ran by Woosley & Weaver (1995) at 
solar metallicity. In doing so, it will default to an upper mass limit on star 
formation of 40 Msun. This is done to minimize numerical artifacts; this is 
the highest mass on the Woosley & Weaver (1995) grid. 

VICE achieves this by calling yields.ccsne.fractional for every 
element built into the software and storing the returned value in 
yields.ccsne.settings.  

set_params :: Update the parameters with which the yields are calculated.  

Notes 
===== 
By importing this module, the user does not sacrifice the flexibility of 
VICE's user-specified yields. After importing this module, the fields of 
vice.yields.ccsne.settings can still be modified in whatever manner the 
user sees fit. 

This module is not import with the simple 'import vice' statement. 

Example 
======= 
>>> from vice.yields.ccsne import WW95 
>>> WW95.set_params(lower = 0.3, upper = 40, IMF = "salpeter") 
"""

from __future__ import absolute_import 
from .. import settings as __settings
from .. import fractional as __fractional
from ...._globals import _RECOGNIZED_ELEMENTS_ 

for i in _RECOGNIZED_ELEMENTS_: 
	__settings[i] = __fractional(i, study = "WW95", m_upper = 40)[0] 
del i 
del absolute_import 


def set_params(**kwargs): 
	"""
	Update the parameters with which the yields are calculated from the 
	Woosley & Weaver (1995) data. 

	Parameters 
	========== 
	kwargs :: varying types 
		Keyword arguments to pass to yields.ccsne.fractional 

	Raises 
	====== 
	TypeError :: 
		::	The user has specified a keyword argument "study". 
	Other exceptions are raised by yields.ccsne.fractional  

	See Also 
	======== 
	yields.ccsne.fractional docstring 

	Example 
	======= 
	>>> from vice.yields.ccsne import WW95 
	>>> WW95.set_params(lower = 0.3, upper = 40, IMF = "salpeter") 

	References 
	========== 
	Woosley & Weaver (1995), ApJ, 101, 181 
	"""
	if "study" in kwargs.keys(): 
		raise TypeError("set_params got an unexpected keyword argument: 'study'") 
	else:
		for i in _RECOGNIZED_ELEMENTS_: 
			__settings[i] = __fractional(i, study = "WW95", **kwargs)[0] 
		del i 


