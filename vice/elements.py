""" 
Elements 
======== 
This module implements convenience functions for elements on the periodic 
table built into VICE. 
""" 

from __future__ import absolute_import 

# __all__ extended at the end of this module out of necessity 
__all__ = ["recognized"] 

from ._globals import _RECOGNIZED_ELEMENTS_ as recognized 
from ._globals import _VERSION_ERROR_ 
from .core.dataframe._builtin_dataframes import stable_isotopes 
from .core.dataframe._builtin_dataframes import atomic_number 
from .core.dataframe._builtin_dataframes import primordial 
from .core.dataframe._builtin_dataframes import solar_z 
from .core.dataframe._builtin_dataframes import sources 
from .yields import ccsne 
from .yields import sneia 
from .yields import agb 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

_FULL_NAMES_ = {
	"c":		"carbon", 
	"n":		"nitrogen", 
	"o":		"oxygen", 
	"f":		"fluorine", 
	"ne":		"neon", 
	"na":		"sodium", 
	"mg":		"magnesium", 
	"al":		"aluminum", 
	"si":		"silicon", 
	"p":		"phosphorous", 
	"s":		"sulfur", 
	"cl":		"chlorine", 
	"ar":		"argon", 
	"k":		"potassium", 
	"ca":		"calcium", 
	"sc":		"scandium", 
	"ti":		"titanium", 
	"v":		"vanadium", 
	"cr":		"chromium", 
	"mn":		"manganese", 
	"fe":		"iron", 
	"co":		"cobalt", 
	"ni":		"nickel", 
	"cu":		"copper", 
	"zn":		"zinc", 
	"ga":		"gallium", 
	"ge":		"germanium", 
	"as":		"arsenic", 
	"se":		"selenium", 
	"br":		"bromine", 
	"kr":		"krypton", 
	"rb":		"rubidium", 
	"sr":		"strontium", 
	"y":		"yttrium", 
	"zr":		"zirconium", 
	"nb":		"niobium", 
	"mo":		"molybdenum", 
	"ru":		"ruthenium", 
	"rh":		"rhodium", 
	"pd":		"palladium", 
	"ag":		"silver", 
	"cd":		"cadmium", 
	"in":		"indium", 
	"sn":		"tin", 
	"sb":		"antimony", 
	"te":		"tellurium", 
	"i":		"iodine", 
	"xe":		"xenon", 
	"cs":		"cesium", 
	"ba":		"barium", 
	"la":		"lanthanum", 
	"ce":		"cerium", 
	"pr":		"praseodymium", 
	"nd":		"neodymium", 
	"sm":		"samarium", 
	"eu":		"europium", 
	"gd":		"gadolinium", 
	"tb":		"terbium", 
	"dy":		"dysprosium", 
	"ho":		"holmium", 
	"er":		"erbium", 
	"tm":		"thulium", 
	"yb":		"ytterbium", 
	"lu":		"lutetium", 
	"hf":		"hafnium", 
	"ta":		"tantalum", 
	"w":		"tungsten", 
	"re":		"rhenium", 
	"os":		"osmium", 
	"ir":		"iridium", 
	"pt":		"platinum", 
	"au":		"gold", 
	"hg":		"mercury", 
	"tl":		"thallium", 
	"pb":		"lead", 
	"bi": 		"bismuth" 
}


def _get_proper_name(element): 
	""" 
	Determines the properly spelled elemental symbol taking into account case. 

	Parameters 
	========== 
	element :: str [case-insensitive] 
		The one- or two-letter symbol for the element as it appears on the 
		periodic table or it's name 

	Returns 
	======= 
	symbol :: str 
		The same string that is passed with the first letter capitalized and 
		all subsequent letters in lower-case. 

	Raises 
	====== 
	TypeError :: 
		::	element is not of type str. 
	""" 
	if isinstance(element, strcomp): 
		sym = element[0].upper() 
		for i in element[1:]: 
			sym += i.lower() 
		return sym 
	else: 
		raise TypeError("Argument must be of type str. Got: %s" % (
			type(element)))


class yields: 

	""" 
	Current Nucleosynthetic yield settings for a given element. 

	Attributes 
	========== 
	ccsne :: float or <function> 
		The current IMF-averaged fracitonal yield from core-collapse 
		supernovae (CCSNe). May be either a constant, real number, or a 
		function of metallicity. 
	sneia :: float or <function> 
		The current IMF-averaged fractional yield from yield from type Ia 
		supernovae (SNe Ia). May be either a constant, real number, or a 
		function of metallicity. 
	agb :: str [case-insensitive] or <function> 
		The current setting for fractional yields from asymptotic giant branch 
		(AGB) stars. May be either a string denoting a built-in yield table 
		from a particular study, or a function of stellar mass in Msun and 
		metallicity by mass (respectively). 

		Recognized AGB study keywords 
		----------------------------- 
		"cristallo11" :: Cristallo et al. (2011), ApJS, 197, 17 
		"karakas10" :: Karakas et al. (2010), MNRAS, 403, 1413 
	""" 

	def __init__(self, symbol): 
		""" 
		Parameters 
		========== 
		symbol :: str [case-insensitive] 
			The elemental symbol 
		""" 
		self._symbol = _get_proper_name(symbol) 

	def __enter__(self): 
		""" 
		Opens a with statement 
		""" 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions inside with statements 
		""" 
		return exc_value is None 

	@property 
	def ccsne(self): 
		""" 
		Type :: real-number or <function>  

		The current nucleosynthetic fractional yield setting for this 
		element from core-collapse supernovae (CCSNe). May be either a real 
		number or a function of metallicity by mass. 

		See Also 	[https://github.com/giganano/VICE/blob/master/docs]
		======== 
		vice.yields.ccsne.fractional 
		Section 5.1 of VICE's science documentation 
		""" 
		return ccsne.settings[self._symbol] 

	@ccsne.setter 
	def ccsne(self, value): 
		# error handling in the yield_settings object 
		ccsne.settings[self._symbol] = value 

	@property 
	def sneia(self): 
		""" 
		Type :: real-number or <function> 

		The current nucleosynthetic fractional yield setting for this 
		element from type Ia supernovae (SNe Ia). May be either a real number 
		or a function of metallicity by mass. 

		See Also 	[https://github.com/giganano/VICE/blob/master/docs] 
		======== 
		vice.yields.sneia.fractional 
		Section 5.2 of VICE's science documentation 
		""" 
		return sneia.settings[self._symbol] 

	@sneia.setter 
	def sneia(self, value): 
		# error handling in the yield_settings object 
		sneia.settings[self._symbol] = value 

	@property 
	def agb(self): 
		""" 
		Type :: str [case-insensitive] or <function> 

		The current nucleosynthetic fractional yield setting for this element 
		from asymptotic giant branch (AGB) stars. May be either a string 
		denoting a built-in yield table from a particular study, or a function 
		of stellar mass in Msun and metallicity by mass (respectively). 

		Recognized AGB study keywords 
		----------------------------- 
		"cristallo11" :: Cristallo et al. (2011), ApJS, 197, 17 
		"karakas10" :: Karakas et al. (2010), MNRAS, 403, 1413 
		""" 
		return agb.settings[self._symbol] 

	@agb.setter 
	def agb(self, value): 
		# error handling in the yield_settings object 
		agb.settings[self._symbol] = value 


class element: 

	""" 
	The core object for an element on the periodic table. 
	""" 
	def __init__(self, symbol): 
		self.symbol = symbol 
		self._yields = yields(self._symbol) 

	def __enter__(self): 
		""" 
		Opens a with statement 
		""" 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions inside with statements 
		""" 
		return exc_value is None 

	def __repr__(self): 
		attrs = {
			"symbol": 				self.symbol, 
			"name": 				_get_proper_name(
										_FULL_NAMES_[self._symbol.lower()]), 
			"atomic number": 		self.atomic_number, 
			"solar abundance": 		self.solar_z, 
			"sources": 				self.sources, 
			"stable isotopes": 		self.stable_isotopes, 
			"primordial": 			self.primordial, 
			"yields.ccsne": 		self.yields.ccsne, 
			"yields.sneia": 		self.yields.sneia, 
			"yields.agb": 			self.yields.agb 
		}

		rep = "vice.element{\n" 
		for i in attrs.keys(): 
			rep += "    %s " % (i) 
			for j in range(18 - len(i)): 
				rep += '-' 
			rep += " > %s\n" % (str(attrs[i])) 
		rep += '}' 
		return rep 

	def __str__(self): 
		return self.__repr__() 

	@property 
	def symbol(self): 
		""" 
		Type :: str 

		The one- or two-letter symbol for the element as it appears on the 
		periodic table. 
		""" 
		return self._symbol 

	@symbol.setter 
	def symbol(self, value): 
		if isinstance(value, strcomp): 
			if value.lower() in recognized: 
				self._symbol = _get_proper_name(value) 
			else: 
				raise ValueError("Unrecognized element: %s" % (value)) 
		else: 
			raise TypeError("""Attribute 'symbol' must be of type str. \
Got: %s""" % (type(value))) 

	@property 
	def yields(self): 
		""" 
		The current yield settings from core-collapse and type Ia supernovae 
		for a chemical element. See each attribute's dostring for more 
		information. 

		Attributes 
		========== 
		ccsne :: real-number or function 
			The current yield setting from core collapse supernovae 
		sneia :: real-number 
			The current yield setting from type Ia supernovae 
		""" 
		return self._yields 

	@property 
	def atomic_number(self): 
		""" 
		Type :: int 

		The atomic number of the element. 
		""" 
		return atomic_number[self._symbol] 

	@property 
	def solar_z(self): 
		""" 
		Type :: real number 

		The solar abundance by mass of the element as calibrated by Asplund 
		et al. (2009), 47, 481. 
		""" 
		return solar_z[self._symbol] 

	@property 
	def sources(self): 
		""" 
		Type :: list [elements of type str] 

		Strings denoting the dominant sources of enrichment for a given 
		element (adopted from Johnson 2019, Science, 6426, 474). 

		Notes 
		===== 
		This does not impact simulations in any manner; yield settings are 
		fully customizable by users. This lookup feature is included purely 
		out of convenience. 
		""" 
		return sources[self._symbol] 

	@property 
	def stable_isotopes(self): 
		""" 
		Type :: list [elements of type int] 

		The stable isotopes of the element 
		""" 
		return stable_isotopes[self._symbol] 

	@property 
	def primordial(self): 
		""" 
		Type :: float 

		The abundance of the element by mass in primordial gas due to 
		big bang nucleosynthesis. 

		In the current implementation, this value is not customizable, and is 
		zero for all elements except helium, for which it is 0.248 
		(Asplund et al. 2009, ARA&A, 47, 481). 
		""" 
		return primordial[self._symbol] 


__all__.extend([_get_proper_name(i) for i in recognized]) 


# Create the element objects 
for i in recognized: 
	exec("%s = element(\"%s\")" % (_get_proper_name(i), i)) 

