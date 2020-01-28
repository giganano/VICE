# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...core import _pyutils 
from . cimport _fitting_function 
from ._parameters cimport parameters 
from ._stepsizes cimport stepsizes 


cdef class fitting_function: 

	def __init__(self, func): 
		self.func = func 

	def __call__(self, time): 
		return self._func(time, *tuple(self._parameters)) 

	@property 
	def func(self): 
		""" 
		Type :: <function> 

		The function to fit to observed data. This attribute may accept any 
		number of real number arguments, the first of which will always be 
		interpreted as time in Gyr. All subsequent arguments will be treated as 
		free parameters to be fit to the data. 
		""" 
		return self._func 

	@func.setter 
	def func(self, value): 
		if callable(value): 
			self._n = _pyutils.arg_count(value) - 1 
			self._parameters = parameters(self._n * [0.]) 
			self._stepsizes = stepsizes(self._n * [0.1]) 
			self._func = value 
		else: 
			raise TypeError("Attribute 'func' must be a callable object.") 

	@property 
	def n(self): 
		""" 
		Type :: int 

		The number of free parameters to be fit to the observed data. 
		""" 
		return self._n 

	@property 
	def parameters(self): 
		""" 
		Type :: list [elements are real numbers] 

		The current value of all fit parameters in the Markov chain. 
		""" 
		return self._parameters 

	@property 
	def stepsizes(self): 
		""" 
		Type :: array-like [elements are real numbers] 

		The stepsizes to take in each fit parameter in the Markov chain. 
		""" 
		return self._stepsizes 

	def take_step(self): 
		""" 
		Move all parameters one step in parameter space. This function will 
		generate a pseudo-random number from a normal distribution whose 
		1-sigma width is given by the stepsizes associated with each parameter, 
		adding that to the current value. 
		""" 
		self._parameters._take_step(self._stepsizes) 

	def revert(self): 
		""" 
		Undo a step in parameter space. This function will revert the current 
		parameters to their immediately previous values. 
		""" 
		self._parameters._revert() 



