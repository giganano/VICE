"""
Asymptotic Giant Branch Star Nucleosynthetic Yield Tools 
======================================================== 
Here users may modify their yield settings from AGB stars, which VICE will 
adopt in their simulations. VICE also provides built-in tables allowing users 
to easy analyze data from previous studies of AGB star nucleosynthesis as well 
as import them directly into their settings. Adopting this setting, VICE 
will adopt a scheme in which the yields are linearly interpolated on a 
2-dimensional table of stellar masses and metallicities reported by the 
study. 

Included Features 
================= 
grid :: <function> 
	Return the stellar mass-metallicity grid of fractional nucleosynethetic 
	yields for a given element and study to the user. 
settings :: VICE dataframe 
	Stores the user's current settings for these yields. 

References 
========== 
Cristallo (2011), ApJS, 197, 17 
Karakas (2010), MNRAS, 403, 1413 
"""

from __future__ import absolute_import
try: 
	__VICE_SETUP__ 
except NameError: 
	__VICE_SETUP__ = False 

if not __VICE_SETUP__: 
	__all__ = ["grid", "settings"] 
	__all__ = [str(i) for i in __all__] 	# appease python 2 strings 

	from ._grid_reader import yield_grid as grid 
	from ...core.dataframe import agb_yield_settings

	settings = agb_yield_settings({ 
		"he": 	"cristallo11", 
		"c":	"cristallo11", 
		"n":	"cristallo11", 
		"o":	"cristallo11", 
		"f":	"cristallo11", 
		"ne":	"cristallo11", 
		"na":	"cristallo11", 
		"mg":	"cristallo11", 
		"al":	"cristallo11", 
		"si":	"cristallo11", 
		"p":	"cristallo11", 
		"s":	"cristallo11", 
		"cl":	"cristallo11", 
		"ar":	"cristallo11", 
		"k":	"cristallo11", 
		"ca":	"cristallo11", 
		"sc":	"cristallo11", 
		"ti":	"cristallo11", 
		"v":	"cristallo11", 
		"cr":	"cristallo11", 
		"mn":	"cristallo11", 
		"fe":	"cristallo11", 
		"co":	"cristallo11", 
		"ni":	"cristallo11", 
		"cu":	"cristallo11", 
		"zn":	"cristallo11", 
		"ga":	"cristallo11", 
		"ge":	"cristallo11", 
		"as":	"cristallo11", 
		"se":	"cristallo11", 
		"br":	"cristallo11", 
		"kr":	"cristallo11", 
		"rb":	"cristallo11", 
		"sr":	"cristallo11", 
		"y":	"cristallo11", 
		"zr":	"cristallo11", 
		"nb":	"cristallo11", 
		"mo":	"cristallo11", 
		"ru":	"cristallo11", 
		"rh":	"cristallo11", 
		"pd":	"cristallo11", 
		"ag":	"cristallo11", 
		"cd":	"cristallo11", 
		"in":	"cristallo11", 
		"sn":	"cristallo11", 
		"sb":	"cristallo11", 
		"te":	"cristallo11", 
		"i":	"cristallo11", 
		"xe":	"cristallo11", 
		"cs":	"cristallo11", 
		"ba":	"cristallo11", 
		"la":	"cristallo11", 
		"ce":	"cristallo11", 
		"pr":	"cristallo11", 
		"nd":	"cristallo11", 
		"sm":	"cristallo11", 
		"eu":	"cristallo11", 
		"gd":	"cristallo11", 
		"tb":	"cristallo11", 
		"dy":	"cristallo11", 
		"ho":	"cristallo11", 
		"er":	"cristallo11", 
		"tm":	"cristallo11", 
		"yb":	"cristallo11", 
		"lu":	"cristallo11", 
		"hf":	"cristallo11", 
		"ta":	"cristallo11", 
		"w":	"cristallo11", 
		"re":	"cristallo11", 
		"os":	"cristallo11", 
		"ir":	"cristallo11", 
		"pt":	"cristallo11", 
		"au":	"cristallo11", 
		"hg":	"cristallo11", 
		"tl":	"cristallo11", 
		"pb":	"cristallo11", 
		"bi":	"cristallo11" 
	}, "AGB yield", True, "agb")

else: 
	pass 

