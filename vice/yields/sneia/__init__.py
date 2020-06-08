r"""
Type Ia Supernovae (SNe Ia) Nucleosynthetic Yield Tools 

Calculate IMF-averaged yields and modify yield settings for use in simulations. 
This package provides tables from the following nucleosynthetic yield studies: 

	- Seitenzahl et al. (2013) [1]_ 
	- Iwamoto et al. (1999) [2]_ 

Contents 
--------
fractional : <function> 
	Calculate an IMF-averaged yield for a given element. 
single : <function> 
	Look up the mass yield of a given element from a single type Ia supernova 
	from a specified study. 
settings : dataframe 
	Stores current settings for these yields. 
seitenzahl13 : yield preset 
	Sets the yields according to the Seitenzahl et al. (2013) study. 
iwamoto99 : yield preset 
	Sets the yields according to the Iwamoto et al. (1999) study. 

.. [1] Seitenzahl et al. (2013), MNRAS, 429, 1156 
.. [2] Iwamoto et al. (1999), ApJ, 124, 439 
"""

from __future__ import absolute_import
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["single", "fractional", "settings", "test"] 
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings 

	from ._yield_lookup import single_detonation as single 
	from ._yield_lookup import integrated_yield as fractional 
	from ...core.dataframe import yield_settings 
	from .tests import test 

	settings = yield_settings({ 
		"he": 	0, 
		"c":	5.74e-6, 
		"n":	6.43e-9, 
		"o":	5.79e-5, 
		"f":	8.21e-14, 
		"ne":	3.38e-6, 
		"na":	4.84e-8, 
		"mg":	8.83e-6, 
		"al":	4.36e-7, 
		"si":	1.41e-4, 
		"p":	3.08e-7, 
		"s":	5.96e-5, 
		"cl":	1.10e-7, 
		"ar":	1.08e-5, 
		"k":	5.26e-8, 
		"ca":	8.94e-6, 
		"sc":	1.13e-10, 
		"ti":	2.52e-7, 
		"v":	7.50e-8, 
		"cr":	9.19e-6, 
		"mn":	1.92e-5, 
		"fe":	2.58e-3, 
		"co":	9.20e-7, 
		"ni":	1.66e-4, 
		"cu":	1.22e-9, 
		"zn":	9.40e-9, 
		"ga":	1.29e-16, 
		"ge":	0, 
		"as":	0, 
		"se":	0, 
		"br":	0, 
		"kr":	0, 
		"rb":	0, 
		"sr":	0, 
		"y":	0, 
		"zr":	0, 
		"nb":	0, 
		"mo":	0, 
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
		"xe":	0, 
		"cs":	0, 
		"ba":	0, 
		"la":	0, 
		"ce":	0, 
		"pr":	0, 
		"nd":	0, 
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
		"hg":	0, 
		"tl":	0, 
		"pb":	0, 
		"bi":	0, 
	}, "SNe Ia yield", False, "sneia")
else: 
	pass 

