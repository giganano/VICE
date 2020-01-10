"""
Asymptotic Giant Branch Star Nucleosynthetic Yield Tools 
========================================================
In the current version of VICE, users are allowed to select 
between two tables of nucleosynthetic yields from asymptotic 
giant branch stars - those published by the Karakas (2010) and 
Cristallo et al. (2011) studies.  

Included Features 
================= 
grid :: <function> 
	Return the stellar mass-metallicity grid of fractional nucleosynethetic 
	yields for a given element and study to the user. 

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
	from ...core._dataframe import agb_yield_settings 

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

