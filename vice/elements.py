r""" 
Chemical Elements 

Provides a means of accessing nucleosynthetic yield information on an 
element-by-element basis. 

.. versionadded:: 1.1.0 

Contents 
--------
recognized : ``tuple`` of strings 
	The symbols of all elements that VICE recognizes as they appear on the 
	periodic table. 
element : ``type`` 
	Provides a means of accessing and modifying relevant information for 
	different elements as well nucleosynthetic yields. 
yields : ``type`` 
	Provides a means of accessing and modifying nucleosynthetic yield settings. 

Element objects can be created from their symbols, or accessed directly 
through VICE's namespace. For example: 

>>> import vice 
>>> vice.elements.Fe 
	vice.element{
		symbol ------------ > Fe
		name -------------- > Iron
		atomic number ----- > 26
		primordial -------- > 0
		solar abundance --- > 0.00129
		sources ----------- > ['CCSNE', 'SNEIA']
		stable isotopes --- > [54, 56, 57, 58]
		yields.ccsne ------ > 0.000246
		yields.sneia ------ > 0.00258
	}
>>> example = vice.elements.element("sr") 
>>> example 
	vice.element{
		symbol ------------ > Sr
		name -------------- > Strontium
		atomic number ----- > 38
		primordial -------- > 0
		solar abundance --- > 4.74e-08
		sources ----------- > ['CCSNE', 'AGB']
		stable isotopes --- > [84, 86, 87, 88]
		yields.ccsne ------ > 1.34e-08
		yields.sneia ------ > 0
	} 
>>> example.symbol = 'fe' 
>>> example 
	vice.element{
		symbol ------------ > Fe
		name -------------- > Iron
		atomic number ----- > 26
		primordial -------- > 0
		solar abundance --- > 0.00129
		sources ----------- > ['CCSNE', 'SNEIA']
		stable isotopes --- > [54, 56, 57, 58]
		yields.ccsne ------ > 0.000246
		yields.sneia ------ > 0.00258
	}

.. seealso:: 
	- vice.yields 
	- vice.atomic_number 
	- vice.primordial 
	- vice.solar_z 
	- vice.sources 
	- vice.stable_isotopes 
""" 

from __future__ import absolute_import 

# __all__ extended at the end of this module out of necessity 
__all__ = ["recognized", "test"]  

from ._globals import _RECOGNIZED_ELEMENTS_ as recognized 
from ._globals import _VERSION_ERROR_ 
from .core.dataframe._builtin_dataframes import stable_isotopes 
from .core.dataframe._builtin_dataframes import atomic_number 
from .core.dataframe._builtin_dataframes import primordial 
from .core.dataframe._builtin_dataframes import solar_z 
from .core.dataframe._builtin_dataframes import sources 
from .tests.elements import test 
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
	"he": 		"helium", 
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


class element: 

	r""" 
	An object describing an element on the periodic table and its astrophysical 
	nucleosynthetic sources and their associated yields. 

	**Signature**: vice.elements.element(symbol) 

	.. versionadded:: 1.1.0 

	Parameters 
	----------
	symbol : ``str`` [case-insensitive] 
		The symbol of the element as it appears on the periodic table. 

	Attributes 
	----------
	symbol : ``str`` 
		The symbol of the element as it appears on the periodic table. 
	name : ``str`` 
		The full name of the element in English. 
	yields : ``yields`` 
		The ``yields`` object containing the nucleosynthetic yield settings 
		for this element. 
	atomic_number : ``int`` 
		The atomic number (protons only) of this element. 
	primordial : ``float`` 
		The primordial abundance by mass of this element according to the 
		standard model [3]_ [4]_ [5]_. 
	solar_z : ``float`` 
		The abundance by mass of this element in the sun as determined by 
		Asplund et al. (2009) [1]_. 
	sources : ``list`` of strings 
		The dominant astrophysical sources of this element as reported by 
		Johnson (2019) [2]_. 
	stable_isotopes : ``list`` of integers 
		The mass numbers (protons and neutrons) of the stable isotopes of 
		this element. 

	.. seealso:: 
		- vice.yields.ccsne.settings 
		- vice.yields.sneia.settings 
		- vice.atomic_number 
		- vice.primordial 
		- vice.solar_z 
		- vice.sources 
		- vice.stable_isotopes 

	Example Code 
	------------
	>>> import vice 
	>>> vice.elements.Fe
		vice.element{
			symbol ------------ > Fe
			name -------------- > Iron
			atomic number ----- > 26
			primordial -------- > 0
			solar abundance --- > 0.00129
			sources ----------- > ['CCSNE', 'SNEIA']
			stable isotopes --- > [54, 56, 57, 58]
			yields.ccsne ------ > 0.000246
			yields.sneia ------ > 0.00258
		}
	>>> example = vice.elements.element("sr") 
	>>> example 
		vice.element{
			symbol ------------ > Sr
			name -------------- > Strontium
			atomic number ----- > 38
			primordial -------- > 0
			solar abundance --- > 4.74e-08
			sources ----------- > ['CCSNE', 'AGB']
			stable isotopes --- > [84, 86, 87, 88]
			yields.ccsne ------ > 1.34e-08
			yields.sneia ------ > 0
		} 
	>>> example.symbol = 'fe' 
	>>> example 
		vice.element{
			symbol ------------ > Fe
			name -------------- > Iron
			atomic number ----- > 26
			primordial -------- > 0
			solar abundance --- > 0.00129
			sources ----------- > ['CCSNE', 'SNEIA']
			stable isotopes --- > [54, 56, 57, 58]
			yields.ccsne ------ > 0.000246
			yields.sneia ------ > 0.00258
		}

	.. [1] Asplund et al. (2009), ARA&A, 47, 481 
	.. [2] Johnson (2019), Science, 363, 474 
	.. [3] Planck Collaboration et al. (2016), A&A, 594, A13
	.. [4] Pitrou et al. (2018), Phys. Rep., 754, 1
	.. [5] Pattie et al. (2018), Science, 360, 627
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
			"name": 				self.name, 
			"atomic number": 		self.atomic_number, 
			"primordial": 			self.primordial, 
			"solar abundance": 		self.solar_z, 
			"sources": 				self.sources, 
			"stable isotopes": 		self.stable_isotopes, 
			"yields.ccsne": 		self.yields.ccsne, 
			"yields.sneia": 		self.yields.sneia 
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
		r""" 
		Type : ``str`` 

		The one- or two-letter symbol of this element as it appears on the 
		periodic table. 

		.. versionadded:: 1.1.0 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Fe.symbol
			'Fe' 
		>>> example = vice.elements.element("sr") 
		>>> example.symbol = "Mg" 
		""" 
		return self._symbol 

	@symbol.setter 
	def symbol(self, value): 
		if isinstance(value, strcomp): 
			if value.lower() in recognized: 
				self._symbol = value.capitalize() 
			else: 
				raise ValueError("Unrecognized element: %s" % (value)) 
		else: 
			raise TypeError("""Attribute 'symbol' must be of type str. \
Got: %s""" % (type(value))) 

	@property 
	def name(self): 
		r""" 
		Type : ``str`` 

		The full name of the element in English. 

		.. versionadded:: 1.1.0 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Mg.name 
			'Magnesium' 
		>>> vice.elements.Sr.name 
			'Strontium' 
		>>> vice.elements.Ne.name 
			'Neon' 
		""" 
		return _FULL_NAMES_[self._symbol.lower()].capitalize() 

	@property 
	def yields(self): 
		r""" 
		The current yield settings from core collapse and type Ia supernovae 
		and asymptotic giant branch stars. See ach attribute's docstring for 
		more information. 

		.. versionadded:: 1.1.0 

		Attributes 
		----------
		ccsne : ``float`` or <function> 
			The current setting for core collapse supernovae. 
		sneia : ``float`` or <function> 
			The current setting for type Ia supernovae. 

		Example Code 
		------------
		>>> import vice
		>>> vice.elements.Fe.yields.sneia 
			0.00258 
		>>> vice.elements.Fe.yields.ccsne = 0.0012 
		>>> vice.yields.ccsne.settings['fe'] 
			0.0012 
		""" 
		return self._yields 

	@property 
	def atomic_number(self): 
		r""" 
		Type : ``int`` 

		The atomic number (protons only) of the element. 

		.. versionadded:: 1.1.0 
		""" 
		return atomic_number[self._symbol] 

	@property 
	def primordial(self): 
		""" 
		Type :: ``float`` 

		The abundance of this element by mass following big bang 
		nucleosynthesis, according to the standard model [1]_ [2]_ [3]_. This 
		is zero for all elements with the exception of helium, for which it is 
		0.24672. 

		.. versionadded:: 1.1.0 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Fe.primordial 
			0 
		>>> vice.elements.He.primordial  
			0.24672 

		.. [1] Planck Collaboration et al. (2016), A&A, 594, A13 
		.. [2] Pitrou et al. (2018), Phys. Rep., 754, 1 
		.. [3] Pattie et al. (2018), Science, 360, 627 
		""" 
		return primordial[self._symbol] 

	@property 
	def solar_z(self): 
		r""" 
		Type : ``float`` 

		The abundance by mass of this element in the sun as reported by 
		Asplund et al. (2009) [1]_. 

		.. versionadded:: 1.1.0 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Fe.solar_z 
			0.00129 
		>>> vice.elements.O.solar_z 
			0.00572 

		.. [1] Asplund et al. (2009), ARA&A, 47, 481 
		""" 
		return solar_z[self._symbol] 

	@property 
	def sources(self): 
		r""" 
		Type : ``list`` of strings 

		Strings denoting the dominant sources of enrichment for this 
		element as reported by Johnson (2019) [1]_. 

		.. versionadded:: 1.1.0 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Fe.sources 
			['CCSNE', 'SNEIA'] 
		>>> vice.elements.Mg.sources 
			['CCSNE'] 

		.. note:: This parameter does not impact simulations in any way. It is 
			purely a look-up function. 

		.. [1] Johnson (2019), Science, 363, 474 
		""" 
		return sources[self._symbol] 

	@property 
	def stable_isotopes(self): 
		r""" 
		Type : ``list`` of integers 

		The mass numbers (protons and neutrons) of the stable isotopes of this 
		element. 

		.. versionadded:: 1.1.0 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Fe.stable_isotopes 
			[54, 56, 57, 58] 
		>>> vice.elements.Mg.stable_isotopes 
			[24, 25, 26] 
		""" 
		return stable_isotopes[self._symbol] 


class yields: 

	r""" 
	Current Nucleosynthetic yield settings for a given element. 

	**Signature**: vice.elements.yields(symbol) 

	.. versionadded:: 1.1.0 

	Parameters 
	----------
	symbol : ``str`` [case-insensitive]	
		The symbol of an element as it appears on the periodic table. 

	Attributes 
	----------
	ccsne : ``float`` or <function> 
		The core collapse supernova yield setting. 
	sneia : ``float`` or <function> 
		The type Ia supernova yield setting. 

	.. note:: modifying yields here is equivalent to modifying them through 
		the vice.yields module. 
	""" 

	def __init__(self, symbol): 
		if isinstance(symbol, strcomp): 
			if symbol.lower() in recognized: 
				self._symbol = symbol.capitalize() 
			else: 
				raise ValueError("Unrecognized element: %s" % (symbol)) 
		else: 
			raise TypeError("Must be of type str. Got: %s" % (type(symbol))) 

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

	# Code masked for future compatability 
	# @property 
	# def agb(self): 
	# 	r""" 
	# 	Type : ``str`` [case-insensitive] or <function> 

	# 	The current yield setting for asymptotic giant branch stars. If this 
	# 	is a string, it will be interpreted as a keyword denoting the built-in 
	# 	table from a nucleosynthesis study to adopt. If this is a <function>, 
	# 	it must accept stellar mass in :math:`M_\odot` as the first parameter 
	# 	and the metallicity by mass :math:`Z` as the second. 

	# 		Keywords and their Associated Studies: 

	# 			- "cristallo11": Cristallo et al. (2011) [1]_ 
	# 			- "karakas10": Karakas (2010) [2]_ 

	# 	Internal yield tables can be analyzed by calling vice.yields.agb.grid. 

	# 	.. note:: Modifying yield settings here is equivalent to modifying 
	# 		vice.yields.agb.settings. 

	# 	.. seealso:: vice.yields.agb.settings 
	# 		vice.yields.agb.grid 

	# 	Example Code 
	# 	------------
	# 	>>> import vice 
	# 	>>> vice.elements.C.yields.agb = "cristallo11" 
	# 	>>> vice.elements.N.yields.agb = "cristallo11" 

	# 	.. [1] Cristallo et al. (2011), ApJS, 197, 17 
	# 	.. [2] Karakas (2010), MNRAS, 403, 1413 
	# 	""" 
	# 	return agb.settings[self._symbol] 

	# @agb.setter 
	# def agb(self, value): 
	# 	# error handling in the yield_settings object 
	# 	agb.settings[self._symbol] = value 

	@property 
	def ccsne(self): 
		r""" 
		Type : real number or <function> 

		The current yield setting for core collapse supernovae (CCSNe). If 
		this is a real number, it will be interpreted as a constant, 
		metallicity-independent yield. If it is a function, it must accept 
		the metallicity by mass :math:`Z` as the only parameter. 

		.. versionadded:: 1.1.0 

		These values can be calculated by calling vice.yields.ccsne.fractional. 

		.. note:: Modifying yield settings here is equivalent to modifying 
			vice.yields.ccsne.settings. 

		.. seealso:: 
			- vice.yields.ccsne.settings 
			- vice.yields.ccsne.fractional 
			- vice.yields.ccsne.table 

		Example Code 
		------------
		>>> import vice
		>>> vice.elements.Fe.yields.ccsne = 0.0012 
		>>> vice.elements.O.yields.ccsne = 0.015 
		""" 
		return ccsne.settings[self._symbol] 

	@ccsne.setter 
	def ccsne(self, value): 
		# error handling in the yield_settings object 
		ccsne.settings[self._symbol] = value 

	@property 
	def sneia(self): 
		r""" 
		Type : real number 

		The current yield setting for type Ia supernovae (SNe Ia). Interpreted 
		as a constant, metallicity-independent yield. 

		.. versionadded:: 1.1.0 

		These values can be calculated by calling vice.yields.sneia.fractional. 

		.. note:: Modifying yield settings here is equivalent to modifying 
			vice.yields.sneia.settings. 

		.. seealso:: 
			- vice.yields.sneia.settings 
			- vice.yields.sneia.fractional 
			- vice.yields.sneia.single 

		Example Code 
		------------
		>>> import vice 
		>>> vice.elements.Fe.yields.sneia = 0.0017 
		>>> vice.elements.O.yields.sneia = 0 
		""" 
		return sneia.settings[self._symbol] 

	@sneia.setter 
	def sneia(self, value): 
		# error handling in the yield_settings object 
		sneia.settings[self._symbol] = value 


__all__.extend([i.capitalize() for i in recognized]) 


# Create the element objects 
for i in recognized: 
	exec("%s = element(\"%s\")" % (i.capitalize(), i)) 

