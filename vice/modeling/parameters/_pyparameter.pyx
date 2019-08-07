# cython: language_level = 3, boundscheck = False
""" 
This file implements the parameter object in VICE. 
""" 

# Python imports 
from __future__ import absolute_import 

__all__ = ["numerical"] 

from ..._globals import _VERSION_ERROR_ 
from ..._globals import ScienceWarning 
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

class numerical: 

	""" 
	Encodes the information associated with model parameters, including 
	whether or not they are allowed to vary 
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
		rep = "vice.modeling.parameter{\n" 
		for i in attrs.keys(): 
			rep += "    %s " % (i) 
			for j in range(15 - len(i)): 
				rep += '-' 
			rep += "> %s\n" % (str(attrs[i])) 
		rep += '}' 
		return rep 

	def __str__(self): 
		return self.__repr__() 

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


