"""
Core Collapse Supernovae Nucleosynthetic Yield Tools 
==================================================== 
Here users can both calculate IMF-integrated nucleosynthetic yields from core 
collapse supernovae as well as modify their yield settings, which VICE will 
adopt in their simulations. VICE has built-in tables allowing users to 
calculate IMF-integrated yields from the results of supernovae simulations ran 
by four different studies, which can also be directly imported as the yield 
settings. 

Included Features 
================ 
fractional :: <function> 
	Calculates IMF-integrated yields of a given element.  
settings :: VICE dataframe 
	Stores the user's current settings for these yields. 

Built-in Yield Tables Available for Import
========================================== 
CL04 :: Chieffi & Limongi (2004) 
CL13 :: Chieffi & Limongi (2013) 
LC18 :: Limongi & Chieffi (2018) 
WW95 :: Woosley & Weaver (1995) 

References 
========== 
Chieffi & Limongi (2004), ApJ, 608, 405 
Chieffi & Limongi (2013), ApJ, 764, 21 
Limongi & Chieffi (2018), ApJS, 237, 13
Woosley & Weaver (1995), ApJ, 101, 181 
"""

from __future__ import absolute_import 
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["fractional", "settings", "table", "test"] 
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings 

	from ._yield_integrator import integrate as fractional 
	from .grid_reader import table 
	from ...core.dataframe import yield_settings 
	from .tests import test 

	settings = yield_settings({ 
		"he": 	0.0616, 
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
	}, "CCSNe yield", True, "ccsne")
else: 
	pass 

