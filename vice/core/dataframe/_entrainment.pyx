# cython: language_level = 3, boundscheck = False 
""" 
This file implements the entrainment settings objects. Every enrichment 
channel in every zone has a zone_entrainment object as an attribute. The data 
stored here represent the mass fractions of various elements that are 
retained by the interstellar medium of a galaxy in a given zone, the remainder 
of which is added directly to outflows. 
""" 

# Python imports 
from __future__ import absolute_import 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _VERSION_ERROR_ 
from ..._globals import _DIRECTORY_ 
from ..._globals import ScienceWarning 
from .. import _pyutils 
import math as m 
import warnings 
import numbers 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _entrainment 


cdef class channel_entrainment(elemental_settings): 

	""" 
	Entrainment settings for a specific enrichment channel. Every element 
	maps to a real number between 0 and 1, representing the mass fraction of 
	that element produced by that enrichment channel which is retained by the 
	interstellar medium. The remainder is added directly to an outflow. 
	""" 

	def __init__(self, frame): 
		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		# super will make sure frame is a dict whose keys are of type str 
		super().__init__(frame) 

	def __setitem__(self, key, value): 
		from ...modeling.singlechain import parameter 
		if isinstance(key, strcomp): 
			if key.lower() in _RECOGNIZED_ELEMENTS_: 
				if isinstance(value, numbers.Number): 
					if 0 <= value <= 1: 
						# allow fitting parameters 
						if isinstance(value, parameter): 
							self._frame[key.lower()] = value 
						else: 
							self._frame[key.lower()] = float(value) 
					else: 
						raise ValueError("""Entrainment fraction must be \
between 0 and 1. Got: %g""" % (value)) 
				else: 
					raise TypeError("""Entrainment fraction must be a \
real number. Got: %s""" % (type(value))) 
			else: 
				raise ValueError("Unrecognized element: %s" % (key)) 
		else: 
			raise TypeError("""Item assignment must be done via type str. \
Got: %s""" % (type(key))) 

