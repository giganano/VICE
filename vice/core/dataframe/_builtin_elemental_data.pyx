# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
import numbers 
from . cimport _builtin_elemental_data 


#----------------- BUILTIN_ELEMENTAL_DATA DATAFRAME SUBCLASS -----------------# 
cdef class builtin_elemental_data(noncustomizable): 

	""" 
	A subclass of the noncustomizable derived class which holds builtin data 
	for each element. 

	See docstring of VICE dataframe base class for more information. 
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

