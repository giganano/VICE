# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ...core import _pyutils 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _dataset 

_RECOGNIZED_WHICH_ = ["stars", "gas"] 

cdef class dataset: 

	def __init__(self, which = "stars"): 
		super().__init__({}) 
		self.which = which 

	def __setitem__(self, key, value): 
		if isinstance(key, strcomp): 
			copy = _pyutils.copy_array_like_object(value) 
			if (len(self.keys()) == 0 or 
				len(copy) == len(self._frame[self.keys()[0]])): 
				self._frame[key.lower()] = copy 
			else: 
				raise ValueError("Array-length mismatch. Got: %d. Needs: %d" % (
					len(copy), len(self._frame[self.keys()[0]]))) 
		else: 
			raise TypeError("""Item assignment only allowed with type str. \
Got: %s""" % (type(key))) 

	def __repr__(self): 
		rep = "%s{\n" % (self.which) 
		for i in super().__repr__().split('\n')[1:]: 
			rep += "    %s\n" % (i) 
		return rep

	def __str__(self): 
		return self.__repr__() 

	@property 
	def which(self): 
		""" 
		Type :: str [always lower-case] 
		Default :: "stars" 

		A string describing the data stored by this object. This is always 
		either "stars" or "gas", denoting stellar or nebular phase abundances, 
		respectively. 
		""" 
		return self._which 

	@which.setter 
	def which(self, value): 
		if isinstance(value, strcomp): 
			if value.lower() in _RECOGNIZED_WHICH_: 
				self._which = value.lower() 
			else: 
				raise ValueError("Unrecognized data type: %s" % (value)) 
		else: 
			raise TypeError("Attribute 'which' must be of type str. Got: %s" % (
				type(value))) 


