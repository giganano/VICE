# cython: language_level = 3, boundscheck = False
""" 
This file implements a subclass of the elemental_settings object. All 
settings are restricted to numerical values and callable functions accepting 
one positional numerical value, which may represent any given quantity for 
an arbitrary element x. 
""" 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from .. import _pyutils 
import numbers 
import sys 
if sys.version[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _evolutionary_settings 


#---------------------- EVOOLUTIONARY SETTINGS SUBCLASS ----------------------#
cdef class evolutionary_settings(elemental_settings): 

	""" 
	A subclass of the elemental_settings subclass which allows only numerical 
	values and functions of time to be assigned to individual elements. 

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
		(The above docstring is entered purely to keep the __init__ docstring 
		consistent across subclasses and instances of the VICE dataframe. 
		Below is the actual docstring for this function.) 

		super() will make sure that frame is a dict with keys of type str that 
		are recognized elements 

		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		name :: str 
			A string denoting the name of the objects stored as fields in 
			this dataframe (i.e. infall metallicity.) 
		""" 
		super().__init__(frame) 
		if isinstance(name, strcomp): 
			self._name = name 
		else: 
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(name))) 

		""" 
		Now make sure that they're all either numerical values or functions of 
		time. 
		""" 
		for i in self.keys(): 
			if isinstance(self._frame[i.lower()], numbers.Number): 
				pass 
			elif callable(self._frame[i.lower()]): 
				_pyutils.args(self._frame[i.lower()], """Functional %s \
setting must take only one numerical parameter.""" % (self._name)) 
			else: 
				raise TypeError("""%s setting must be either a numerical \
value or a callable function accepting one numerical parameter. Got: %s""" % (
					self._name, type(self._frame[i.lower()]))) 

	def __setitem__(self, key, value): 
		from ...modeling.singlechain import parameter 
		if isinstance(key, strcomp): 
			if key.lower() in _RECOGNIZED_ELEMENTS_: 
				if isinstance(value, numbers.Number): 
					# allow fitting parameters 
					if isinstance(value, parameter): 
						self._frame[key.lower()] = value 
					else: 
						self._frame[key.lower()] = float(value) 
				elif callable(value): 
					_pyutils.args(value, """Functional %s setting must \
accept only one numerical parameter.""" % (self._name)) 
					self._frame[key.lower()] = value 
				else: 
					raise TypeError("""%s setting must be either a numerical \
value or a function accepting one numerical parameter. Got: %s""" % (
						self._name, type(key)))   
			else: 
				raise ValueError("Unrecognized element: %s" % (key)) 
		else: 
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key))) 


	def remove(self, key): 
		""" 
		This function throws a TypeError whenever called. This derived class 
		of the VICE dataframe does not support item deletion. 
		""" 
		# Suppring item deletion here could break singlezone simulations 
		raise TypeError("This dataframe does not support item deletion.") 

