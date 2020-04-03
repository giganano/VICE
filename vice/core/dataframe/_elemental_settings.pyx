# cython: language_level = 3, boundscheck = False
""" 
This file handles the implementation of the elemental_settings subclass of the 
VICE dataframe. These only allow __getitem__ via strings of elemental symbols 
case-insensitively. 
""" 

from ..._globals import _VERSION_ERROR_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
	input = raw_input 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _elemental_settings 


#---------------------------- ELEMENTAL SETTINGS ----------------------------# 
cdef class elemental_settings(base): 

	""" 
	A subclass of the VICE dataframe which only allows keys that are the 
	symbols of elements built into VICE [case-insensitive]. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	def __init__(self, frame): 
		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		# super will make sure frame is a dict whose keys are of type str 
		super().__init__(frame) 

		# Now make sure each keys is a recognized element 
		for i in self.keys(): 
			if i.lower() not in _RECOGNIZED_ELEMENTS_: 
				raise ValueError("Unrecognized element: %s" % (i)) 
			else: 
				continue 

	def __getitem__(self, key): 
		if isinstance(key, strcomp): 
			if key.lower() in self.keys(): 
				return self._frame[key.lower()] 
			else: 
				raise KeyError("Unrecognized element: %s" % (key)) 
		else: 
			raise IndexError("Dataframe key must be of type str. Got: %s" % (
				type(key))) 


	def remove(self, key): 
		""" 
		This function throws a TypeError whenever called. This derived class 
		of the VICE dataframe does not support item deletion. 
		""" 
		# Allowing this could let user's break their own singlezone objects 
		raise TypeError("This dataframe does not support item deletion.") 


	def filter(self, key, relation, value): 
		""" 
		This function throws a TypeError whenever called. This derived class 
		of the VICE dataframe does not support filtering. 

		.. seealso:: vice.dataframe.filter 
		""" 
		raise TypeError("This dataframe does not support the filter function.") 

