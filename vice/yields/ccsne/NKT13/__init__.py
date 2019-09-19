""" 
Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457 Nucleosynthetic Yield Tools 
=============================================================================== 
Importing this module will automatically set all yield settings from core 
collapse supernovae to the IMF-integrated yields as determined from the 
simulations ran by Nomoto, Kobayashi & Tominaga (2013) at Z = 0.02 ([M/H] = 
+0.15 if Zsun = 0.014 from Asplund et al. (2009), ARA&A, 47, 481). In doing 
so, it will default to an upper mass limit on star formation of 40 Msun. This 
is done to minimize numerical artifacts; this is the highest mass on the 
Nomoto, Kobayashi & Tominaga (2013) grid. 

VICE achieves this by calling yields.ccsne.fractional for every element 
built into the software and storing the returned value in 
yields.ccsne.settings. 

set_params :: Update the parameters with which they yields are calculated 

Notes 
===== 
At Z = 0 ([M/H] = -inf), the yield grid is sampled up to 300 Msun. 

By importing this module, the user does not sacrifice the flexibility of 
VICE's user-specified yields. After importing this module, the fields of 
vice.yields.ccsne.settings can still be modified in whatever manner the 
user sees fit. 

This module is not import with the simple 'import vice' statement. 

Example 
======= 
>>> from vice.yields.ccsne import NKT13 
>>> NKT13.set_params(lower = 0.3, upper = 45, IMF = "salpeter") 
""" 

from __future__ import absolute_import 
from .. import settings as __settings 
from .. import fractional as __fractional 
from ...._globals import _RECOGNIZED_ELEMENTS_ 

for i in _RECOGNIZED_ELEMENTS_: 
	__settings[i] = __fractional(i, study = "NKT13", m_upper = 40, 
		MoverH = 0.15)[0] 
del i 
del absolute_import 

def set_params(**kwargs): 
	""" 
	Update the parameters with which the yields are calculated from the 
	Nomoto, Kobayashi & Tominaga (2013) data. 

	Parameters 
	========== 
	kwargs :: varying types 
		Keyword arguments to pass to yields.ccsne.fractional 

	Raises 
	====== 
	TypeError :: 
		::	The user has specified a keyword argument "study" 
	Other exceptions are raised by yields.ccsne.fractional 

	See Also 
	======== 
	yields.ccsne.fractional docstring 

	Example 
	======= 
	>>> from vice.yields.ccsne import NKT13 
	>>> NKT13.set_params(lower = 0.3, upper = 45, IMF = "salpeter") 

	References 
	========== 
	Nomoto, Kobayashi & Tominaga (2013), ARA&A, 51, 457 
	""" 
	if "study" in kwargs.keys(): 
		raise TypeError("set_params got an unexpected keyword argument: 'study'") 
	else: 
		for i in _RECOGNIZED_ELEMENTS_: 
			__settings[i] = __fractional(i, study = "NKT13", **kwargs)[0] 
		del i 

