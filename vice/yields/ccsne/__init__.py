# This file, included with the VICE package, is protected under the terms of the 
# associated MIT License, and any use or redistribution of this file in original 
# or altered form is subject to the copyright terms therein. 

"""
Core Collapse Supernovae Nucleosynthetic Yield Tools 
==================================================== 
Here users can both calculate IMF-integrated nucleosynthetic yields from CCSNe 
as well as modify their adopted settings, which VICE will adopt in their 
simulations. VICE has built-in tables allowing users to calculate 
IMF-integrated yields from the results of supernovae simulations ran by 
Woosley & Weaver (1995), Chieffi & Limongi (2004), Chieffi & Limongi (2013), 
and Limongi & Chieffi (2018). 

Inclued Features 
================ 
fractional :: <function> 
	Calculates IMF-integrated yields of a given element 
settings :: VICE dataframe 
	Stores the user's current settings these yields. 

References 
========== 
Chieffi & Limongi (2004), ApJ, 608, 405 
Chieffi & Limongi (2013), ApJ, 764, 21 
Limongi & Chieffi (2018), ApJS, 237, 13
Woosley & Weaver (1995) ApJ, 101, 181 
"""

from __future__ import absolute_import
from .yield_integrator import integrate as fractional
from ...core._data_utils import _customizable_yield_table 
import sys 

__all__ = ["fractional", "settings"] 
__all__ = [str(i) for i in __all__] # appease python 2 strings 

settings = _customizable_yield_table({
	"c":	2.36e-3, 
	"n":	5.78e-4, 
	"o":	5.64e-3, 
	"f":	5.15e-8, 
	"ne":	1.75e-3, 
	"na":	4.08e-5, 
	"mg":	4.97e-4, 
	"al":	4.89e-5, 
	"si":	7.52e-4, 
	"p":	6.13e-6, 
	"s":	2.88e-4, 
	"cl":	2.67e-6, 
	"ar":	5.36e-5, 
	"k":	9.55e-7, 
	"ca":	4.12e-5, 
	"sc":	2.26e-8, 
	"ti":	8.53e-7, 
	"v":	8.75e-8, 
	"cr":	3.88e-6, 
	"mn":	3.61e-6, 
	"fe":	2.46e-4, 
	"co":	5.43e-6, 
	"ni":	5.59e-4, 
	"cu":	6.42e-7, 
	"zn":	4.89e-6, 
	"ga":	9.70e-8, 
	"ge":	1.67e-7, 
	"as":	1.24e-8, 
	"se":	5.91e-8, 
	"br":	6.15e-9, 
	"kr":	3.42e-8, 
	"rb":	5.89e-9, 
	"sr":	1.34e-8, 
	"y":	2.47e-9, 
	"zr":	5.06e-9, 
	"nb":	3.10e-10, 
	"mo":	9.87e-10, 
	"ru":	0, 
	"rh":	0, 
	"pd":	0, 
	"ag":	0, 
	"cd":	0, 
	"in":	0, 
	"sn":	0, 
	"sb":	0, 
	"te":	0, 
	"i":	0, 
	"xe":	1.04e-9, 
	"cs":	2.01e-10, 
	"ba":	2.80e-9, 
	"la":	2.37e-10, 
	"ce":	6.07e-10, 
	"pr":	9.24e-11, 
	"nd":	3.06e-10, 
	"sm":	0, 
	"eu":	0, 
	"gd":	0, 
	"tb":	0, 
	"dy":	0, 
	"ho":	0, 
	"er":	0, 
	"tm":	0, 
	"yb":	0, 
	"lu":	0, 
	"hf":	0, 
	"ta":	0, 
	"w":	0, 
	"re":	0, 
	"os":	0, 
	"ir":	0, 
	"pt":	0, 
	"au":	0, 
	"hg":	1.39e-10, 
	"tl":	8.53e-7, 
	"pb":	1.50e-9, 
	"bi":	1.17e-10
}, True, "ccsne")

del absolute_import 
del yield_integrator
del _customizable_yield_table
if sys.version_info[0] < 3: 
	del i 
else:
	pass 

