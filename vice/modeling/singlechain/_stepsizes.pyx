# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
import numbers 
from . cimport _stepsizes 

cdef class stepsizes: 

	def __init__(self, arr): 
		if all(map(lambda x: isinstance(x, numbers.Number), arr)): 
			self._arr = [float(i) for i in arr] 
		else: 
			raise TypeError("All elements must be real numbers.") 

	def __getitem__(self, key): 
		if isinstance(key, numbers.Number): 
			if key % 1 == 0: 
				if 0 <= key < len(self._arr): 
					return self._arr[int(key)] 
				elif -len(self._arr) <= key < 0: 
					return self._arr[len(self._arr) + key] 
				else: 
					raise IndexError("Index out of bounds: %g" % (key)) 
			else: 
				raise IndexError("""Index must be interpretable as an integer. \
Got: %g""" % (key)) 
		else: 
			raise IndexError("Index must be of type int. Got: %s" % (type(key))) 

	def __setitem__(self, key, value): 
		if isinstance(key, numbers.Number): 
			if key % 1 == 0: 
				if isinstance(value, numbers.Number): 
					self._arr[int(key)] = float(value) 
				else: 
					raise TypeError("""Stepsize must be a numerical value. \
Got: %s""" % (type(value))) 
			else: 
				raise ValueError("""Index must be interpretable as an integer. \
Got: %g""" % (key)) 
		else: 
			raise TypeError("Index must be of type int. Got: %s" % (type(key))) 

	def __repr__(self): 
		return "stepsizes(%s)" % (str(self._arr)) 

	def __str__(self): 
		return self.__repr__() 

	def __len__(self): 
		""" 
		Returns the number of parameters whose stepsizes are stored in this 
		object. 
		""" 
		return len(self._arr) 


