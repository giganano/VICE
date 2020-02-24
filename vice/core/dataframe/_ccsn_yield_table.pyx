# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = ["ccsn_yield_table"] 
import numbers 
from . cimport _ccsn_yield_table 
from ._base cimport base 


cdef class ccsn_yield_table: 

	""" 
	A subclass of the VICE dataframe designed to hold the data from a 
	CCSN yield table lookup. These objects can be indexed via either stellar 
	mass or isotope name, if the table was created with the keyword 
	isotopic = True. 
	""" 


	def __init__(self, masses, yields, isotopes = None): 
		# Store the masses, yields and isotopes as attributes 
		super().__init__({}) 
		if all(map(lambda x: isinstance(x, numbers.Number), masses)): 
			self._masses = tuple(masses[:]) 
		else: 
			raise SystemError("Internal Error") 
		if isotopes is not None: 
			self._isotopes = tuple(isotopes[:]) 
			if all(map(lambda x: isinstance(x, tuple), yields)): 
				for i in yields: 
					if not all(map(lambda x: isinstance(x, numbers.Number), 
						i)): 
						raise SystemError("Internal Error") 
					else: 
						continue 
				self._yields = tuple(yields[:]) 
			else: 
				raise SystemError("Internal Error") 
		else: 
			if all(map(lambda x: isinstance(x, numbers.Number), yields)): 
				self._yields = tuple(yields[:]) 
			else: 
				raise SystemError("Internal Error") 


	def __repr__(self): 
		rep = "vice.dataframe{\n" 
		if self._isotopes is not None: 
			for i in range(len(self._masses)): 
				rep += "    %g " % (self._masses[i]) 
				for j in range(15 - len("%g" % (self._masses[i]))): 
					rep += "-" 
				rep += "> %s\n" % (str(dict(zip(
					self._isotopes, 
					[j[i] for j in self._yields]
				))))
		else: 
			for i in self._masses: 
				rep += "    %s " % (str(i)) 
				for j in range(15 - len(str(i))): 
					rep += "-" 
				rep += "> %s\n" % (str(self.__getitem__(i))) 
		rep += "}" 
		return rep 


	def __subget__str(self, key): 
		""" 
		Override the base __getitem__ functionality for isotope lookup 
		""" 
		if self._isotopes is not None: 
			if key.lower() in self._isotopes: 
				yields = self._yields[self._isotopes.index(key.lower())] 
				return ccsn_yield_table(self._masses, yields, isotopes = None) 
			else: 
				raise IndexError("Unrecognized isotope: %s" % (key)) 
		else: 
			raise TypeError("This yields dataframe is not isotopic.") 


	def __subget__number(self, key): 
		""" 
		Override the base __getitem__ functionality for stellar mass lookup 
		""" 
		if key in self._masses: 
			if self._isotopes is not None: 
				idx = self._masses.index(key)  
				yields = [i[idx] for i in self._yields] 
				return base(dict(zip(self._isotopes, yields))) 
			else: 
				return self._yields[self._masses.index(key)] 
		else: 
			raise IndexError("Mass not on grid: %g" % (key)) 

	def __setitem__(self, key, value): 
		raise TypeError("This dataframe is not customizable") 


	@property 
	def masses(self): 
		""" 
		Type :: tuple 

		The masses in Msun on the table 
		""" 
		return self._masses 


	@property 
	def isotopes(self): 
		""" 
		Type :: tuple 

		The stable isotopes whose yields are sampled. None if the table was 
		generated with isotopic = False. 
		""" 
		return self._isotopes 


	def keys(self): 
		""" 
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		if self._isotopes is not None: 
			return list(self._isotopes) 
		else: 
			return list(self._masses) 


	def todict(self): 
		""" 
		Signature: vice.dataframe.todict() 

		Returns the dataframe as a standard python dictionary. Note however 
		that python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		""" 
		return dict(zip( 
			self.keys(), 
			[self.__getitem__(i) for i in self.keys()]
		))

