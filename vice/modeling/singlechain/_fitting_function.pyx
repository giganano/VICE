# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...core import _pyutils 
from . cimport _fitting_function 
from ._parameters cimport parameters 


cdef class fitting_function: 

	""" 
	An object containing the functional form and parameters of a numerical 
	model to be fit to external data. 

	Attributes 
	========== 
	function :: <function> 
		The functional form of the model to be fit to the data. 
	n :: int [automatically assigned] 
		The number of numerical parameters to be fit to the function. 
	parameters :: parameters object 
		The numerical parameters to be fit to the data 

	Functions 
	========= 
	take_step :: 
		Update each parameter by adding a pseudorandom number drawn from a 
		normal distribution. 
	revert :: 
		Undo the most recent call to take_step 

	Notes 
	===== 
	This function is callable with only one numerical argument, allowing it 
	to be assigned to the 'func' attribute of the singlezone object. 
	""" 

	def __init__(self, func): 
		self.function = func 

	def __call__(self, time): 
		return self._function(time, *tuple(self._parameters)) 

	@property 
	def function(self): 
		""" 
		Type :: <function> 

		The function to fit to observed data. This attribute may accept any 
		number of real number arguments, the first of which will always be 
		interpreted as time in Gyr. All subsequent arguments will be treated as 
		free parameters to be fit to the data. 
		""" 
		return self._function 

	@function.setter 
	def function(self, value): 
		if callable(value): 
			self._n = _pyutils.arg_count(value) - 1 
			self._parameters = parameters(self._n * [0.]) 
			self._function = value 
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
		Type :: parameters object  

		An array-like object containing each numerical parameter to be fit to 
		the data, its current value, and its stepsize. 
		""" 
		return self._parameters 

	def take_step(self): 
		""" 
		Move all parameters one step in parameter space. This function will 
		generate a pseudo-random number from a normal distribution whose 
		1-sigma width is given by the stepsizes associated with each parameter, 
		adding that to the current value. 
		""" 
		self._parameters.take_step() 

	def revert(self): 
		""" 
		Undo the previous call to take_step(), reverting all parameters to 
		their immediately previous values. 
		""" 
		self._parameters.revert() 

