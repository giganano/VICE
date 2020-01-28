# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from . cimport _parameters 

cdef class parameters: 

	def __init__(self, arr): 
		_parameters.seed_random() 
		super().__init__(arr) 

	def __repr__(self): 
		return "parameters(%s)" % (str(self._arr)) 

	def _take_step(self, stepsizes): 
		assert self.__len__() == len(stepsizes) 
		self._old = self._arr[:] 
		for i in range(self.__len__()): 
			self._arr[i] += _parameters.normal(0, stepsizes[i]) 

	def _revert(self): 
		for i in range(self.__len__()): 
			self._arr[i] = self._old[i] 


