""" 
Elements 
======== 
This module implements convenience functions for elements on the periodic 
table built into VICE. 
""" 

from __future__ import absolute_import 

# __all__ initialized at the end of this module out of necessity 

from .._globals import _RECOGNIZED_ELEMENTS_ 
from .._globals import _VERSION_ERROR_ 
from ..core.dataframe._builtin_dataframes import atomic_number 
from ..core.dataframe._builtin_dataframes import solar_z 
from ..core.dataframe._builtin_dataframes import sources 
from ..yields import agb 
from ..yields import ccsne 
from ..yields import sneia 
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
	""" 
	if isinstance(element, strcomp): 
		sym = element[0].upper() 
		for i in element[1:]: 
			sym += i.lower() 
		return sym 
	else: 
		raise TypeError("Argument must be of type str. Got: %s" % (
			type(element)))


class yields(object): 

	def __init__(self, symbol): 
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
		Type :: real-number or function 

		The current nucleosynthetic yields setting for the current element 
		from core-collapse supernovae. 

		See Also 	[https://github.com/giganano/VICE/blob/master/docs]
		======== 
		Section 5.1 of VICE's science documentation 
		""" 
		return ccsne.settings[self._symbol] 

	@ccsne.setter 
	def ccsne(self, value): 
		# error handling in the dataframe root class 
		ccsne.settings[self._symbol] = value 

	@property 
	def sneia(self): 
		""" 
		Type :: real-number 

		The current nucleosynthetic yield setting for the current element 
		from type Ia supernovae. 

		See Also 	[https://github.com/giganano/VICE/blob/master/docs] 
		======== 
		Section 5.2 of VICE's science documentation 
		""" 
		return sneia.settings[self._symbol] 

	@sneia.setter 
	def sneia(self, value): 
		# error handling in the dataframe root class 
		sneia.settings[self._symbol] = value 


class element(object): 

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
			"symbol": 			self.symbol, 
			"name": 			_get_proper_name(
									_FULL_NAMES_[self._symbol.lower()]), 
			"atomic_number": 	self.atomic_number, 
			"solar_z": 			self.solar_z, 
			"sources": 			self.sources, 
			"yields.ccsne": 	self.yields.ccsne, 
			"yields.sneia": 	self.yields.sneia 
		}

		rep = "vice.element{\n" 
		for i in attrs.keys(): 
			rep += "    %s " % (i) 
			for j in range(15 - len(i)): 
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
			if value.lower() in _RECOGNIZED_ELEMENTS_: 
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

		Strings denoting what astronomers generally believe to be the dominant 
		enrichment sources for each element adopted from Johnson (2019), 
		Science, 6426, 474. 
		""" 
		return sources[self._symbol] 


__all__ = [_get_proper_name(i) for i in _RECOGNIZED_ELEMENTS_] 


# Create the element objects for __all__ 
for i in _RECOGNIZED_ELEMENTS_: 
	exec("%s = element(\"%s\")" % (_get_proper_name(i), i)) 

