# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...core import _pyutils 
import numbers 
import copy 
from . cimport _parameters 

cdef class parameters: 

	""" 
	A list of parameters whose primary purpose is to fit a functional form of a 
	numerical model to external data. 

	Functions 
	========= 
	take_step :: 
		Update each parameter by adding a pseudorandom number drawn from a 
		normal distribution. 
	revert :: 
		Undo calls to take_step() 
	""" 

	def __init__(self, arr): 
		try: 
			self._parameters = len(arr) * [None] 
		except TypeError: 
			raise TypeError("Must be an array-like object. Got: %s" % (
				type(arr))) 
		for i in range(self.__len__()): 
			self._parameters[i] = parameter(arr[i]) 

	def __getitem__(self, key): 
		if isinstance(key, numbers.Number): 
			if key % 1 == 0: 
				if 0 <= key < self.__len__(): 
					return self._parameters[int(key)] 
				elif -self.__len__() <= key < 0: 
					return self._parameters[self.__len__() + int(key)] 
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
				if 0 <= key < self.__len__(): 
					idx = int(key) 
				elif -self.__len__() <= key < 0: 
					idx = self.__len__() + int(key) 
				else: 
					raise IndexError("""Item assignment index out of bounds: \
%g""" % (key)) 
				if isinstance(value, parameter): 
					self._parameters[idx] = value 
				elif isinstance(value, numbers.Number): 
					self._parameters[idx] = parameter(
						value = float(value), 
						stepsize = self._parameters[idx].stepsize
					) 
				else: 
					raise TypeError("""Item assignment must be either a \
numerical value or a parameter object.""") 
			else: 
				raise ValueError("""Index must be interpretable as an integer. \
Got: %g""" % (key)) 
		else: 
			raise TypeError("Index must be of type int. Got: %s" % (type(key))) 

	def __repr__(self): 
		return str(self._parameters) 

	def __str__(self): 
		return self.__repr__() 

	def __len__(self): 
		return len(self._parameters) 

	def take_step(self): 
		""" 
		Update all parameters by adding pseudorandom numbers drawn from 
		normal distributions. 

		See Also 
		======== 
		vice.modeling.parameter.stepsize 
		vice.modeling.parameter.new 
		""" 
		for i in range(self.__len__()): 
			self.__setitem__(i, self._parameters[i].new()) 

	def revert(self): 
		""" 
		Undo calls to take_step(). 

		Raises 
		====== 
		RuntimeError :: 
			::	take_step() has not been called yet, or cannot be undone 
				further. 

		See Also 
		======== 
		vice.modeling.parameters.old 
		""" 
		for i in range(self.__len__()): 
			self.__setitem__(i, self._parameters[i].old())  


class parameter(float): 

	""" 
	Contains basic information on an arbitrary numerical parameter whose 
	primary function is to be fit to external data. Inherits from the built-in 
	float class. 

	Signature: vice.modeling.parameter.__init__(
		value = 0, 
		stepsize = 0.1 
	)

	Attributes 
	========== 
	stepsize :: float [default :: 0.1] 
		The 1-sigma width of the gaussian distribution to draw pseudo-random 
		numbers from in modifying the attribute 'value'. 

	Functions 
	========= 
	step :: 
		Add a pseudorandom number drawn from a normal distribution whose width 
		is given by the attribute 'stepsize' and return a new parameter object. 
	""" 

	def __new__(cls, value = 0, stepsize = 0.1): 
		return float.__new__(cls, value) 

	def __init__(self, value = 0, stepsize = 0.1): 
		float.__init__(value) 
		self.stepsize = stepsize 
		self._previous = None 
		_parameters.seed_random() 

	def __repr__(self): 
		return "parameter(value = %g, stepsize = %g)" % (
			self.real, 
			self.stepsize
		) 

	def __str__(self): 
		return self.__repr__() 

	def __iadd__(self, other): 
		return parameter(
			value = self.__add__(other), 
			stepsize = self.stepsize
		) 

	def __isub__(self, other): 
		return parameter(
			value = self.__sub__(other), 
			stepsize = self.stepsize
		) 

	def __imul__(self, other): 
		return parameter(
			value = self.__mul__(other), 
			stepsize = self.stepsize
		) 

	def __ifloordiv__(self, other): 
		return parameter(
			value = self.__floordiv__(other), 
			stepsize = self.stepsize
		) 

	def __idiv__(self, other): 
		return parameter(
			value = self.__div__(other), 
			stepsize = self.stepsize 
		) 

	def __itruediv__(self, other): 
		return parameter(
			value = self.__truediv__(other), 
			stepsize = self.stepsize 
		) 

	def __imod__(self, other): 
		return parameter(
			value = self.__mod__(other), 
			stepsize = self.stepsize
		) 

	def __ipow__(self, other): 
		return parameter(
			value = self.__pow__(other), 
			stepsize = self.stepsize 
		) 

	@property 
	def stepsize(self): 
		return self._stepsize 

	@stepsize.setter 
	def stepsize(self, value): 
		if isinstance(value, numbers.Number): 
			if value: 
				self._stepsize = float(value) 
			else: 
				raise ValueError("Attribute 'stepsize' must be nonzero.") 
		else: 
			raise TypeError("""Attribute 'stepsize' must be a real number. \
Got: %s""" % (type(value))) 

	def new(self): 
		""" 
		Obtain a new parameter by adding a pseudorandom number generated from a 
		normal distribution to the current parameter. The width of the normal 
		distribution is set by the attribute 'stepsize'. 

		Returns 
		======= 
		new :: parameter 
			The modified parameter 
		""" 
		new = parameter(
			value = self.real + _parameters.normal(0, self.stepsize), 
			stepsize = self.stepsize 
		) 
		new._previous = self 
		return new 

	def old(self): 
		""" 
		Obtain the parameter that generated another via a call to new(). 

		Returns 
		======= 
		old :: parameter 
			The parameter whose call to new() generated this parameter. 

		Raises 
		====== 
		RuntimeError :: 
			::	This parameter was instantiated directly, rather than by a 
				call to new(). 
		""" 
		if self._previous is not None: 
			return self._previous 
		else: 
			raise RuntimeError("""Could not revert further. This parameter \
was instantiated directly, not from another parameter. """) 

