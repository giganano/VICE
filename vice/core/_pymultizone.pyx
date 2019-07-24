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
from ._migration_matrix import migration_matrix 
from ..yields import agb 
from ..yields import ccsne 
from ..yields import sneia 
from . import _dataframe as df 
from . import _pyutils 
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

cdef class migration_specifications: 

	""" 
	Migration specifications for multizone simulations. 
	""" 

	cdef object _stars 
	cdef object _gas 

	def __init__(self, int n): 
		self._stars = migration_matrix(n) 
		self._gas = migration_matrix(n) 

	def __repr__(self): 
		rep = "ISM: " 
		for i in str(self._gas).split('\n'): 
			rep += "    %s\n" % (i) 
		for i in range(22): 
			rep += ' '
		rep += "Stars: "
		for i in str(self._stars).split('\n'): 
			rep += "    %s\n" % (i) 
		rep += "" 
		return rep 

	def __str__(self): 
		return self.__repr__() 

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

	@property 
	def gas(self): 
		""" 
		The migration matrix associated with the interstellar gas. 

		Contains user-specified migration prescriptions for use in multizone 
		simulations. For a multizone simulation with N zones, this is an NxN 
		matrix. 

		This matrix is defined such that the ij'th element represents the 
		likelihood that interstellar gas or stars will migrate FROM the i'th 
		TO the j'th zone in the simulation. These entries may be either 
		numerical values or functions of time in Gyr. In all cases, the value 
		at a given time must be between 0 and 1, because the elements are 
		interpreted as likelihoods. 
		""" 
		return self._gas 

	@property 
	def stars(self): 
		""" 
		The migration matrix associated with the stars. 

		Contains user-specified migration prescriptions for use in multizone 
		simulations. For a multizone simulation with N zones, this is an NxN 
		matrix. 

		This matrix is defined such that the ij'th element represents the 
		likelihood that interstellar gas or stars will migrate FROM the i'th 
		TO the j'th zone in the simulation. These entries may be either 
		numerical values or functions of time in Gyr. In all cases, the value 
		at a given time must be between 0 and 1, because the elements are 
		interpreted as likelihoods. 
		""" 
		return self._stars 


cdef class multizone: 

	""" 
	Wrapping of the C version of the multizone object. 
	""" 

	cdef MULTIZONE *_mz 
	cdef object _zones 
	cdef migration_specifications _migration 

	def __cinit__(self, n_zones = 10): 
		if isinstance(n_zones, numbers.Number): 
			if n_zones > 0: 
				if n_zones % 1 == 0: 
					n_zones = int(n_zones) 
					self._mz = _multizone.multizone_initialize(n_zones) 
					self._zones = n_zones * [None] 
					for i in range(n_zones): 
						self._zones[i] = singlezone() 
						self._zones[i].name = "zone%d" % (i) 
						_multizone.link_zone(self._mz, 
							self._zones[i]._singlezone__zone_object_address(), 
							i) 
				else: 
					# error handled in __init__ 
					pass 
			else: 
				# error handled in __init__ 
				pass 
		else: 
			# error handled in __init__ 
			pass 

	def __init__(self, n_zones = 10, 
		name = "multizonemodel", 
		n_tracers = 1, 
		verbose = False): 
		
		if isinstance(n_zones, numbers.Number): 
			if n_zones > 0: 
				if n_zones % 1 == 0: 
					self.name = name 
					self._migration = migration_specifications(n_zones) 
					self.n_tracers = n_tracers 
					self.verbose = verbose 
				else: 
					raise ValueError("""Attribute 'n_zones' must be an \
integer. Got: %g""" % (n_zones)) 
			else: 
				raise ValueError("Attribute 'n_zones' must be positive.") 
		else: 
			raise TypeError("""Attribute 'n_zones' must be a numerical value. \
Got: %s""" % (type(n_zones))) 

	def __dealloc__(self): 
		_multizone.multizone_free(self._mz) 

	def __repr__(self): 
		""" 
		Prints in the format: vice.singlezone{ 
			attr1 -----------> value 
			attribute2 ------> value 
		}
		""" 
		attrs = {
			"name": 			self.name, 
			"n_zones": 			self.n_zones, 
			"n_tracers": 		self.n_tracers, 
			"verbose": 			self.verbose, 
			"migration": 		self.migration 
		} 

		rep = "vice.multizone{\n" 
		for i in attrs.keys(): 
			rep += "    %s " % (i) 
			for j in range(15 - len(i)): 
				rep += '-' 
			rep += "> %s\n" % (str(attrs[i])) 
		rep += '}' 
		return rep 

	def __str__(self): 
		return self.__repr__() 

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

	@property 
	def n_zones(self): 
		# docstring in python version 
		return self._mz[0].n_zones 

	@property 
	def n_tracers(self): 
		# docstring in python version 
		return self._mz[0].n_tracers 

	@n_tracers.setter 
	def n_tracers(self, value): 
		""" 
		The number of tracer particles per zone per timestep 

		Allowed Types 
		============= 
		real number 

		Allowed Values 
		============== 
		Positive integers 
		""" 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				if value % 1 == 0: 
					self._mz[0].n_tracers = int(value) 
				else: 
					raise ValueError("""Attribute 'n_tracers' must be \
interpretable as an integer. Got: %g""" % (value)) 
			else: 
				raise ValueError("""Attribute 'n_tracers' must be positive. \
Got: %g""" % (value)) 
		else: 
			raise TypeError("""Attribute 'n_tracers' must be an integer. \
Got: %s""" % (type(value))) 

	@property 
	def verbose(self): 
		# docstring in python version 
		return bool(self._mz[0].verbose) 

	@verbose.setter 
	def verbose(self, value): 
		""" 
		Whether or not to print the time as the simulation evolves. 

		Allowed Types 
		============= 
		bool 

		Allowed Values 
		============== 
		True and False 
		""" 
		if isinstance(value, numbers.Number) or isinstance(value, bool): 
			if value: 
				self._mz[0].verbose = 1 
			else: 
				self._mz[0].verbose = 0 
		else: 
			raise TypeError("""Attribute 'verbose' must be interpretable as \
a boolean. Got: %s""" % (type(value))) 

	@property 
	def migration(self): 
		# docstring in python version 
		return self._migration 


