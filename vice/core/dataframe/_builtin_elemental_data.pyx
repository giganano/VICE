# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
import numbers 
from . cimport _builtin_elemental_data 


#----------------- BUILTIN_ELEMENTAL_DATA DATAFRAME SUBCLASS -----------------# 
cdef class builtin_elemental_data(noncustomizable): 

	r""" 
	The VICE dataframe: derived class (inherits from noncustomizable) 

	Stores persistent data for each element. 

	Allowed Data Types 
	------------------
	* Keys 
		- ``str`` [case-insensitive] : elemental symbols 
			The symbols of the elements as they appear on the periodic table. 

	* Values 
		- Any (cannot be modified) 

	Indexing 
	--------
	- ``str`` [case-insensitive] : elemental symbols 
		Must be indexed by the symbol of an element recognized by VICE as it 
		appears on the periodic table. 

	Functions 
	---------
	- keys 
	- todict 

	Built-In Instances 
	------------------
	- vice.atomic_number 
		The atomic number (protons only) of each element. 
	- vice.primordial 
		The primordial abundance by mass :math:`Z` of each element following 
		big bang nucleosynthesis. This is zero for all elements with the 
		exception of helium, which is assigned the standard model value of 
		:math:`Y_\text{p} = 0.24672 \pm 0.00017` [1]_ [2]_ [3]_. 
	- vice.solar_z 
		The abundance by mass of each element in the sun. This is adopted from 
		Asplund et al. (2009) [4]_. 
	- vice.sources 
		The dominant astrophysical enrichment channels of each element. This 
		is adopted from Johnson (2019) [5]_. 
	- vice.stable_isotopes 
		The mass number (protons + neutrons) of the stable isotopes of each 
		element. 

	Example Code 
	------------
	>>> import vice 
	>>> vice.atomic_number['c'] 
		6
	>>> vice.primordial['c'] 
		0 
	>>> vice.solar_z['c'] 
		0.00236 
	>>> vice.sources['c'] 
		["CCSNE", "AGB"] 
	>>> vice.stable_isotopes['c'] 
		[12, 13] 

	.. [1] Planck Collaboration et al. (2016), A&A, 594, A13 
	.. [2] Pitrou et al. (2018), Phys. Rep., 754, 1 
	.. [3] Pattie et al. (2018), Science, 360, 627 
	.. [4] Asplund et al. (2009), ARA&A, 47, 481 
	.. [5] Johnson (2019), Science, 363, 474 
	""" 

	def __init__(self, frame, name): 
		"""
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 

		"""
		super will make sure frame is a dict, that all keys are recognized 
		elements, and that name is a string 
		"""
		super().__init__(frame, name) 

		"""
		Instances of this class store built-in data. At present, they must be 
		either numerical values or of type list. 
		""" 
		for i in self.keys(): 
			if not (isinstance(self._frame[i.lower()], numbers.Number) or 
				isinstance(self._frame[i.lower()], list)): 
				raise TypeError("""%s settings must be either a numerical \
value or a list. Got: %s""" % (self._name, type(self._frame[i.lower()]))) 
			else: 
				continue 

