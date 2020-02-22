# cython: language_level = 3, boundscheck = False
""" 
This file handles the implementation of the base class of the VICE dataframe. 
The most distinguishing feature of the VICE dataframe from other dataframes 
such as that of Pandas is that the VICE dataframe is case-insensitive, while 
retaining the ability to index based on either column label or row number. 
""" 

from __future__ import absolute_import  
from ..._globals import _VERSION_ERROR_ 
from .. import _pyutils 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _base 


#------------------------- VICE DATAFRAME BASE CLASS -------------------------#
cdef class base: 

	"""
                                 The VICE Dataframe 
	==========================================================================
	Provides a means of storing data indexed by strings in a case-insensitive 
	manner. VICE includes several instances of this class at the global level, 
	some of which have features specific to their instance. Users may call 
	these dataframes as a function using parentheses rather than square 
	brackets and it will return the same thing. If a dataframe stores 
	array-like attributes, it may also be indexed via an integer to pull that 
	element from each field. 

	Signature: vice.dataframe.__init__(frame) 

	Functions
	=========
	keys		
	todict 

	Yield Setting Dataframes 
	======================== 
	The following dataframes store the user's settings for nucleosynthetic 
	yields from core collapse and type Ia supernovae. In the case of 
	core collapse supernovae yields, the user may specify a function 
	accepting one numerical parameter, which will be interpreted as the 
	metallicity by mass Z of the stellar population. 

	yields.ccsne.settings :: Yield settings from core collapse supernovae 
	yields.sneia.settings :: Yield settings from type Ia supernovae 

	Functions Associated with these Dataframes 
	------------------------------------------ 
	factory_defaults :: Revert to VICE's original defaults 
	restore_defaults :: Revert to user's specified defaults 
	save_defaults :: Save current settings as defaults 

	Other Built-in dataframes 
	========================= 
	VICE provides the following dataframes. 

	atomic_number
	------------- 
	Stores the number of protons in the nucleus of each of VICE's recognized 
	elements. By design, this dataframe does not support item assignment 

	primordial 
	---------- 
	Stores the abundance by mass of each element in the primordial universe 
	following big bang nucleosynthesis. In the current version, this value is 
	only nonzero for helium. 

	solar_z 
	-------  
	Stores the abundance by mass of elements in the sun. By nature, this 
	dataframe does not support user customization. Solar abundances are 
	derived from Asplund et al. (2009) and have been converted to a mass 
	fraction via: 

		Z_x,sun = (mu_x)(X_sun)10^((X/H) - 12) 

	where mu_x is the mean molecular weight of the element in amu, X_sun is 
	the solar hydrogen abundance by mass, and (X/H) = log10(Nx/NH) + 12, 
	which is what Asplund et al. (2009) reports. These calculations adopt 
	X_sun = 0.73 as the solar hydrogen abundances, also from Asplund et al. 
	(2009). 

	sources 
	-------  
	Stores strings denoting what astronomers generally believe to be the 
	dominant enrichment channels for each element. These are included purely 
	for convenience, and are adopted from Johnson (2019). This dataframe does 
	not support user customization.

		Enrichment Channels 
		------------------- 
		"CCSNE" :: core collapse supernovae 
		"SNEIA" :: type Ia supernovae 
		"AGB" :: asymptotic giant branch stars 
		"NSNS" :: binary neutron star mergers / r-process 

	References 
	========== 
	Asplund et al. (2009), ARA&A, 47, 481 
	Johnson (2019), Science, 6426, 474 
	"""

	# cdef object _frame 

	def __init__(self, frame): 
		""" 
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		if isinstance(frame, dict): 
			if all(map(lambda x: isinstance(x, strcomp), frame.keys())): 
				keys = tuple([i.lower() for i in frame.keys()]) 
				fields = tuple([frame[i] for i in frame.keys()]) 
				self._frame = dict(zip(keys, fields)) 
			else: 
				raise TypeError("All keys must be of type str.") 
		else: 
			raise TypeError("""Can only initialize dataframe from type dict. \
Got: %s""" % (type(frame))) 

	def __call__(self, key): 
		""" 
		Return the same thing as __getitem__ ---> this allows users to call 
		the dataframe and achieve the same effect. 
		""" 
		return self.__getitem__(key) 

	def __getitem__(self, key): 
		""" 
		If type str, index the dataframe on key.lower(). This allows 
		case-insensitivity. If an integer, will attempt to pull the proper 
		row from a dataframe containing array-like attributes. 

		In this case, the returned value will also be a dataframe. 
		""" 
		if isinstance(key, strcomp): # index via column label 
			return self.__subget__str(key) 
		elif isinstance(key, numbers.Number): # index via row number 
			return self.__subget__number(key) 
		else: 
			raise IndexError("""Only integers and strings are valid indeces. \
Got: %s""" % (type(key))) 

	def __subget__str(self, key): 
		""" 
		Performs the __getitem__ operation when the key is a string. 
		""" 
		if key.lower() in self.keys(): 
			return self._frame[key.lower()] 
		else: 
			raise KeyError("Unrecognized dataframe key: %s" % (key)) 

	def __subget__number(self, key): 
		""" 
		Performs the __getitem__ operation when the key is a number 
		""" 
		if key % 1 == 0: 
			# index by int only works when all fields are array-like 
			try: 
				lengths = [len(self._frame[i]) for i in self.keys()] 
			except TypeError: 
				raise IndexError("""This dataframe cannot be indexed by a key \
of type int, because not all fields are array-like.""") 

			# This if condition allows -key to pass if -key == min(lengths) 
			if abs(key) <= min(lengths) and key != min(lengths): 
				return base(dict(zip(self.keys(), 
					[self._frame[i][int(key)] for i in self.keys()]
				))) 
			else: 
				raise IndexError("Index out of bounds: %d" % (int(key))) 

		else: 
			raise IndexError("""Index must be interpreted as an integer. \
Got: %s""" % (type(key))) 

	def __setitem__(self, key, value): 
		""" 
		__setitem__ only allowed given a string. 
		""" 
		if isinstance(key, strcomp): 
			self._frame[key.lower()] = value 
		else: 
			raise TypeError("""Item assignment must be done via type str. \
Got: %s""" % (type(key))) 

	def __repr__(self): 
		"""
		Fancy print of the format: 
		vice.dataframe{ 
		    field1 --------> value1 
		    field_other ---> value2
		}
		"""	
		rep = "vice.dataframe{\n" 
		keys = self.keys() 
		copy = self.todict() 
		for i in keys: 
			rep += "    %s " % (i) 
			arrow = "" 
			# terminate each arrow at the same point 
			for j in range(15 - len(i)): 
				arrow += '-' 
			rep += "%s> " % (arrow) 
			try: 
				x = _pyutils.copy_array_like_object(copy[i]) 
			except TypeError: 
				x = copy[i] 
				rep += "%s\n" % (str(x)) 
				continue 
			# only array-like objects make it here 
			if len(x) >= 10: 
				rep += "[%g, %g, %g, ... , %g, %g, %g]\n" % (
					x[0], x[1], x[2], x[-3], x[-2], x[-1]) 
			else: 
				rep += "%s\n" % (str(x)) 
		rep += '}'
		return rep 

	def __str__(self): 
		""" 
		Returns self.__repr__() 
		""" 
		return self.__repr__() 
			
	def __eq__(self, other): 
		""" 
		Returns True if the dataframes have the same contents. In the case of 
		dataframes instantiated off of VICE outputs (i.e. history, mdf, and 
		output objects), returns True if they came from the same file. 
		""" 
		test = len(self.keys()) * [None] 
		for i in range(len(self.keys())): 
			try: 
				test[i] = other[self.keys()[i]] 
			except KeyError: 
				return False 
		if all(list(map(lambda x: test[x] == self._frame[self.keys()[x]], 
			range(len(self.keys()))))): 
			return True 
		else:
			return False 

	def __ne__(self, other): 
		""" 
		Returns not self.__eq__(other) 
		""" 
		return not self.__eq__(other) 

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

	def keys(self): 
		"""
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		return [i.lower() for i in self._frame.keys()] 

	def todict(self): 
		"""
		Signature: vice.dataframe.todict() 

		Returns the dataframe as a standard python dictionary. Note however 
		that python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		""" 
		return self._frame 

	def remove(self, key): 
		""" 
		Remove an element of the dataframe 

		Signature: vice.dataframe.remove(key) 

		Parameters 
		========== 
		key :: str [case-insensitive] 
			The dataframe key to remove 

		Raises 
		====== 
		KeyError :: 
			::	Invalid dataframe key 
		""" 
		if key.lower() in self._frame.keys(): 
			del self._frame[key.lower()] 
		else: 
			raise KeyError("Unrecognized dataframe key: %s" % (key)) 

