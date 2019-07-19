# cython: language_level = 3, boundscheck = False
""" 
This file implements the python wrapper of the multizone object, which runs 
simulations under the singlezone approximation. Most of the subroutins are in 
C, found in the vice/src/ directory within the root tree. 
""" 

# Python imports 
from __future__ import absolute_import 
from .._globals import _RECOGNIZED_ELEMENTS_ 
from .._globals import _RECOGNIZED_IMFS_ 
from .._globals import _VERSION_ERROR_ 
from .._globals import _DEFAULT_FUNC_ 
from .._globals import _DEFAULT_BINS_ 
from .._globals import _DIRECTORY_ 
from .._globals import ScienceWarning 
from ._builtin_dataframes import atomic_number 
from ._builtin_dataframes import solar_z 
from ._builtin_dataframes import sources 
from ._output import output 
from ._pysinglezone import _RECOGNIZED_MODES_ 
from ._pysinglezone import _RECOGNIZED_DTDS_ 
from ._pysinglezone import singlezone 
from ..yields import agb 
from ..yields import ccsne 
from ..yields import sneia 
from . import _dataframe as df 
from . import _pyutils 
import math as m 
import warnings 
import numbers 
import inspect 
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
try: 
	"""
	dill extends the pickle module and allows functional attributes to be 
	encoded. In later versions of python 3, dill.dump must be called instead 
	of pickle.dump. All cases can be taken care of by overriding the native 
	pickle module and letting dill masquerade as pickle. 
	""" 
	import dill as pickle 
except (ModuleNotFoundError, ImportError): 
	pass 

# C imports 
from libc.stdlib cimport malloc, realloc, free 
from libc.string cimport strlen, strcpy 
from ._objects cimport AGB_YIELD_GRID 
from ._objects cimport CCSNE_YIELD_SPECS 
from ._objects cimport SNEIA_YIELD_SPECS 
from ._objects cimport ELEMENT 
from ._objects cimport ISM 
from ._objects cimport MDF 
from ._objects cimport SSP 
from ._objects cimport SINGLEZONE 
from ._objects cimport TRACER 
from ._objects cimport MULTIZONE 
from . cimport _agb 
from . cimport _ccsne 
from . cimport _cutils 
from . cimport _element 
from . cimport _io 
from . cimport _mdf 
from . cimport _multizone 
from . cimport _singlezone 
from . cimport _sneia 
from . cimport _ssp 

cdef class multizone: 

	""" 
	Wrapping of the C version of the multizone object. 
	""" 

	cdef MULTIZONE *_mz 
	cdef object _zones 

	def __cinit__(self, int n): 
		if n > 0: 
			self._mz = _multizone.multizone_initialize(n) 
			self._zones = n * [None] 
			for i in range(n): 
				self._zones[i] = singlezone() 
				self._zones[i]._sz = self._mz[0].zones[i] 
				self._zones[i].name = "zone%d" % (i) 
		else: 
			raise ValueError("Number of zones must be positive. Got: %d" % (n)) 

	def __init__(self, int n, name = "multizonemodel"): 
		self.name = name 

	def __dealloc__(self): 
		_multizone.multizone_free(self._mz) 

	@property 
	def zones(self): 
		# docstring in python version 
		return self._zones 

	@property 
	def name(self): 
		# docstring in python version 
		return "".join([chr(self._mz[0].name[i]) for i in range(
			strlen(self._mz[0].name))])[:-5] 

	@name.setter 
	def name(self, value): 
		""" 
		Name of the simulation, also the directory that the output is written 
		to. 

		Allowed Types 
		============= 
		str 

		Allows Values 
		============= 
		Simple strings, or those of the format 'path/to/dir' 

		All values will pass the setter except for empty strings. Those that 
		are not valid directory names will fail at runtime when self.run() is 
		called. 
		""" 
		if isinstance(value, strcomp): 
			if _pyutils.is_ascii(value): 
				if len(value) == 0: 
					raise ValueError("""Attribute 'name' must not be an \
empty string.""") 
				else: 
					pass 
				while value[-1] == '/': 
					# remove any '/' that the user puts on 
					value = value[:-1] 
				if value.lower().endswith(".vice"): 
					# force the .vice extension to lower-case 
					value = "%s.vice" % (value[:-5]) 
				else: 
					value = "%s.vice" % (value) 
				_cutils.set_string(self._mz[0].name, value) 
			else: 
				raise ValueError("String must be ascii. Got: %s" % (value)) 
		else: 
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(value))) 





