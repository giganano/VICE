# cython: language_level = 3, boundscheck = False
""" 
This file implements the parameter object in VICE. 
""" 

# Python imports 
from __future__ import absolute_import 

__all__ = ["numerical", "functional"]  

from ..._globals import _VERSION_ERROR_ 
from ..._globals import ScienceWarning 
from ...core import _pyutils 
import math as m 
import warnings 
import numbers 
import pickle 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 

# C imports 
from libc.stdlib cimport malloc, free 
from ._objects cimport NUMPARAM 
from . cimport _numparam
from . cimport _utils 

""" 
NOTES 
===== 
cdef class objects do not transfer the docstrings of class attributes to the 
compiled output, leaving out the internal documentation. For this reason, 
wrapping of the parameter object has two layers -> a python class and a 
C class. In the python class, there is only one attribute: the C version of 
the wrapper. The docstrings are written here, and each function/setter 
only calls the C version of the wrapper. While this is a more complicated 
wrapper, it preserves the internal documentation. In order to maximize 
readability, the setter functions of the C version of the wrapper have brief 
notes on the physical interpretation of each attribute as well as the allowed 
types and values. 
""" 


class functional: 

	""" 
	Encodes the informatin associated with functional model parameters, 
	including their numerical attributes and whether or not each of them are 
	allowed to vary 
	""" 

	def __init__(self, generator, n): 
		if isinstance(n, numbers.Number): 
			if n % 1 == 0: 
				self._n = int(n) 
			else: 
				raise ValueError("Attribute 'n' must be an integer.") 
		else: 
			raise TypeError("Attribute 'n' must be an integer. Got: %s" % (
				type(n))) 
		self._params = self._n * [None] 
		for i in range(self._n): 
			self._params[i] = numerical(0) 
		self.generator = generator 	# call the setter function 

	def __call__(self, value): 
		return self._current(value) 

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

	def __repr__(self): 
		rep = "vice.modeling.parameters.functional{\n" 
		attrs = {
			"n":			self.n, 
			"generator": 	self.generator, 
		}
		for i in attrs.keys(): 
			rep += "    %s " % (i) 
			for j in range(15 - len(i)): 
				rep += '-' 
			rep += "> %s\n" % (str(attrs[i])) 
		for i in range(self.n): 
			rep += "    parameters[%d] " % (i) 
			for j in range(15 - len("parameters[%d]" % (i))): 
				rep += '-' 
			rep += "> current = %.5e\n" % (self.parameters[i].current) 
			for j in range(22): 
				rep += ' '
			rep += "varies = %s\n" % (self.parameters[i].varies) 
			for j in range(22): 
				rep += ' '
			rep += "stepsize = %.5e\n" % (self.parameters[i].stepsize) 
		rep += '}' 
		return rep 

	def __str__(self): 
		return self.__repr__() 

	@property 
	def n(self): 
		""" 
		The number of numerical parameters associated with this functional 
		parameter 
		""" 
		return self._n 

	# @n.setter 
	# def n(self, value): 
	# 	if isinstance(value, numbers.Number): 
	# 		if value % 1 == 0: 
	# 			if value < self._n: 
	# 				self._n = int(value) 
	# 				self._params = self._params[:self._n] 
	# 			elif value > self._n: 
	# 				self._params.extend((value - self._n) * [None]) 
	# 				for i in range(self._n, value): 
	# 					self._params[i] = numerical(0) 
	# 				self._n = int(value) 
	# 			else: 
	# 				# value == self._n 
	# 				pass 
	# 		else: 
	# 			raise ValueError("Attribute 'n' must be an integer.") 
	# 	else: 
	# 		raise TypeError("Attribute 'n' must be an integer. Got: %s" % (
	# 			type(value))) 

	@property 
	def parameters(self): 
		""" 
		The numerical parameters associated with this functional parameter 
		""" 
		return self._params 

	@property 
	def generator(self): 
		""" 
		The generator function for this functional attribute 
		""" 
		return self._generator 

	@generator.setter 
	def generator(self, value): 
		if callable(value): 
			args = [float(i) for i in self._params] 
			try: 
				value(*args) 
			except TypeError: 
				# incorrect number of arguments -> improper generator function 
				raise ValueError("""Attribute 'generator' must be a function \
which accepts attribute 'n' number of parameters. Expected number of \
arguments: %d.""" % (self._n)) 
			if callable(value(*args)): 
				_pyutils.args(value(*args), """Attribute 'generator' must \
return a function which accepts one numerical parameter.""") 
				self._generator = value 
				self._refresh() 
			else: 
				raise ValueError("""Attribute 'generator' must be a function \
which returns a callable function. Got: %s""" % (type(value(*args)))) 
		else: 
			raise TypeError("""Attribute 'generator' must be a callable \
function. Got: %s""" % (type(value))) 

	@property 
	def current(self): 
		return self._current 

	# @current.setter 
	def _refresh(self): 
		self._current = self._generator(*[float(i) for i in self._params]) 

	def step(self): 
		for i in range(self._n): 
			self._params[i].step() 
		self._refresh() 





class numerical: 

	""" 
	Encodes the information associated with numerical model parameters, 
	including whether or not they are allowed to vary 
	""" 

	def __init__(self, start, let_vary = False): 
		if isinstance(let_vary, numbers.Number) or isinstance(let_vary, bool): 
			if let_vary: 
				let_vary = int(1) 
			else: 
				let_vary = int(0) 
			if isinstance(start, numbers.Number): 
				start = float(start) 
				self.__c_version = c_numerical(start, let_vary) 
			else: 
				raise TypeError("""Attribute 'current' must be a real number. \
Got: %s""" % (type(start))) 
		else: 
			raise TypeError("""Attribute 'varies' must be interpretable as a \
boolean. Got: %s""" % (type(let_vary))) 

	def __enter__(self): 
		""" 
		Opens a with statement 
		""" 
		return self.__c_version.__enter__() 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions that occur inside with statements 
		""" 
		return self.__c_version.__exit__(exc_type, exc_value, exc_tb) 

	def __repr__(self): 
		return self.__c_version.__repr__() 

	def __str__(self): 
		return self.__c_version.__str__() 

	def __float__(self): 
		return self.__c_version.__float__() 

	@property 
	def current(self): 
		""" 
		Type :: real number 

		The current value of the parameter in the markov chain 
		""" 
		return self.__c_version.current 

	@current.setter 
	def current(self, value): 
		self.__c_version.current = value 

	@property 
	def varies(self): 
		""" 
		Type :: bool 
		Default :: False 

		Whether or not this parameter varies between subsequence elements of 
		the MCMC chain (i.e. whether or not it's best-fit value is being 
		determined). 
		""" 
		return self.__c_version.varies 

	@varies.setter 
	def varies(self, value): 
		self.__c_version.varies = value 

	@property 
	def stepsize(self): 
		""" 
		Type :: real number 
		Default :: 0.1 

		The 1-sigma gaussian stepsize to take in this parameter between 
		subsequent elements of the markov chain. 

		Only relevant when varies = True 
		""" 
		return self.__c_version.stepsize 

	@stepsize.setter 
	def stepsize(self, value): 
		self.__c_version.stepsize = value 

	def step(self): 
		""" 
		Let the parameter take a step via a gaussian-random number
		""" 
		self.__c_version.step()  


cdef class c_numerical: 

	""" 
	Encodes the information associated with model parameters, including 
	whether or not they are allowed to vary 
	""" 
	cdef NUMPARAM *_p 

	def __cinit__(self, start, let_vary): 
		assert isinstance(let_vary, int), "Internal Error" 
		assert isinstance(start, float), "Internal Error" 
		self._p = _numparam.numparam_initialize(<double> start, 
			<unsigned short> let_vary) 
		_utils.seed_random()  

	def __init__(self, start, let_vary): 
		assert isinstance(let_vary, int), "Internal Error" 
		assert isinstance(start, float), "Internal Error" 

	def __dealloc__(self): 
		_numparam.numparam_free(self._p) 

	def __enter__(self): 
		""" 
		Opens a with statement 
		""" 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions that occur inside with statements 
		""" 
		return exc_value is None 

	def __repr__(self): 
		attrs = {
			"current": 			self.current, 
			"varies": 			self.varies, 
			"stepsize": 		self.stepsize 
		} 
		rep = "vice.modeling.parameters.numerical{\n" 
		for i in attrs.keys(): 
			rep += "    %s " % (i) 
			for j in range(15 - len(i)): 
				rep += '-' 
			rep += "> %s\n" % (str(attrs[i])) 
		rep += '}' 
		return rep 

	def __str__(self): 
		return self.__repr__() 

	def __float__(self): 
		return self._p[0].current 

	@property 
	def varies(self): 
		# docstring in python version 
		return bool(self._p[0].varies) 

	@varies.setter 
	def varies(self, value): 
		""" 
		Whether or not the parameter varies with time 

		Allowed Types 
		=============
		bool 

		Allowed Values 
		============== 
		True and False 
		""" 
		if isinstance(value, numbers.Number) or isinstance(value, bool): 
			if value: 
				self._p[0].varies = <unsigned short> 1 
			else: 
				self._p[0].varies = <unsigned short> 0 
		else: 
			raise TypeError("""Attribute 'varies' must be interpretable as a \
boolean. Got: %s""" % (type(value))) 

	@property 
	def stepsize(self): 
		# docstring in python version 
		return self._p[0].stepsize 

	@stepsize.setter 
	def stepsize(self, value): 
		""" 
		The 1-sigma gaussian stepsize to take in this parameter in MCMC fitting 

		Allowed Types 
		============= 
		real number 

		Allowed Values 
		============== 
		> 0 
		""" 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				self._p[0].stepsize = <double> value 
			else: 
				raise ValueError("""Attribute 'stepsize' must be positive \
definite.""") 
		else: 
			raise TypeError("""Attribute 'stepsize' must be a real number. \
Got: %s""" % (type(value))) 

	@property 
	def current(self): 
		# docstring in python version 
		return self._p[0].current 

	@current.setter 
	def current(self, value): 
		""" 
		The current value of the parameter 

		Allowed Types 
		============= 
		real number 

		Allowed Values 
		============== 
		all 
		""" 
		if isinstance(value, numbers.Number): 
			self._p[0].current = <double> value 
		else: 
			raise TypeError("""Attribute 'current' must be a real number. \
Got: %s""" % (type(value))) 

	def step(self): 
		""" 
		Let the parameter take a step via a gaussian-random number 
		""" 
		_numparam.numparam_step(self._p) 

