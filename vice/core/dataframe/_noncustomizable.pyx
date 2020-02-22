# cython: language_level = 3, boundscheck = False
""" 
This file implements the noncustomizable dataframe, a subclass of the 
elemental_settings object. These do not allow item assignment for any 
element whatsoever. The only objects of this type are built-in data, and 
hold either numerical values or lists. 
""" 

from ..._globals import _VERSION_ERROR_ 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _noncustomizable 


#-------------------- NONCUSTOMIZABLE DATAFRAME SUBCLASS --------------------#
cdef class noncustomizable(elemental_settings): 

	""" 
	A subclass of the elemental_settings subclass which throws a TypeError 
	whenever __setitem__ is called. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	# cdef object _name 

	def __init__(self, frame, name): 
		"""
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 

		"""
		super will make sure frame is a dict and that all keys are recognized 
		elements. 
		"""
		super().__init__(frame) 
		if isinstance(name, strcomp): 
			self._name = name 
		else: 
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(name))) 

		"""
		Instances of this class store built-in data. They must be either 
		numerical values or of type list. 
		""" 
		for i in self.keys(): 
			if not (isinstance(self._frame[i.lower()], numbers.Number) or 
				isinstance(self._frame[i.lower()], list)): 
				raise TypeError("""%s settings must be a numerical value or a \
list. Got: %s""" % (type(self._frame[i.lower()]))) 
			else: 
				continue 

	def __setitem__(self, key, value): 
		"""
		Override the base __setitem__ function to throw a TypeError whenever 
		this function is called. 
		""" 
		raise TypeError("This dataframe does not support item assignment.") 


	def remove(self, key): 
		""" 
		This function throws a TypeError whenever called. This derived class 
		of the VICE dataframe does not support item deletion. 
		""" 
		# Noncustomizability also means not being able to remove anything 
		raise TypeError("This dataframe does not support item deletion.") 

