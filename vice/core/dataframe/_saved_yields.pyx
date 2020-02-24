# cython: language_level = 3, boundscheck = False
""" 
This file implements the saved_yields object, a subclass of the VICE dataframe 
which is designed to hold saved nucleosynthetic yields. For that reason, it is 
noncustomizable. 
""" 

from ..._globals import _VERSION_ERROR_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from . cimport _saved_yields


#--------------------------- SAVED YIELDS SUBCLASS ---------------------------# 
cdef class saved_yields(noncustomizable): 

	""" 
	A subclass of the VICE dataframe which holds the user's settings from 
	core collapse and type Ia supernovae at the time a singlezone simulation 
	was ran. 

	By nature, this class throws a TypeError every time __setitem__ is called. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	def __init__(self, frame, name): 
		"""
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 

		"""
		super will make sure frame is a dict and that all keys are recognized 
		elements. 
		"""
		super().__init__(frame, name) 

		""" 
		Saved yields will have already passed the necessary type-checking 
		filters, so just make sure everything in the output looks okay. No 
		need for _pyutils.args. 
		""" 
		for i in self.keys(): 
			if not (
				isinstance(self._frame[i.lower()], numbers.Number) or 
				isinstance(self._frame[i.lower()], strcomp) or 
				callable(self._frame[i.lower()]) 
			): 
				raise TypeError("""%s yield setting must be either a \
numerical value, callable function, or string. Got: %s""" % (self._name, 
					type(self._frame[i.lower()]))) 
			else: 
				continue 

