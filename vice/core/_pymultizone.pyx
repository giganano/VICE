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
from . cimport _migration 
from . cimport _multizone 
from . cimport _singlezone 
from . cimport _sneia 
from . cimport _ssp 

cdef class multizone: 

	""" 
	Wrapping of the C version of the multizone object. 
	""" 

	cdef MULTIZONE *_mz 
	cdef zone_array _zones 
	cdef migration_specifications _migration 

	def __cinit__(self, 
		n_zones = 10, 
		name = "multizonemodel", 
		n_tracers = 1, 
		verbose = False): 
		if isinstance(n_zones, numbers.Number): 
			if n_zones > 0: 
				if n_zones % 1 == 0: 
					n_zones = int(n_zones) 
					self._mz = _multizone.multizone_initialize(n_zones) 
					self._zones = zone_array(n_zones) 
					for i in range(n_zones): 
						_multizone.link_zone(self._mz, 
							self._zones[i]._singlezone__zone_object_address(), 
							i) 
					# self._zones = n_zones * [None] 
					# for i in range(n_zones): 
					# 	self._zones[i] = singlezone() 
					# 	self._zones[i].name = "zone%d" % (i) 
					# 	_multizone.link_zone(self._mz, 
					# 		self._zones[i]._singlezone__zone_object_address(), 
					# 		i) 
				else: 
					# error handled in __init__ 
					pass 
			else: 
				# error handled in __init__ 
				pass 
		else: 
			# error handled in __init__ 
			pass 

	def __init__(self, 
		n_zones = 10, 
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

	def run(self, output_times, capture = False, overwrite = False): 
		""" 
		To-do list for this function 
		============================ 
		migration matrices need piped to C 
		need to interpret value of enrichment variable once it's done: it's 
			not a simple "1 if failed setup" as in singlezone 
		""" 
		self.align_name_attributes() 
		self.prep(output_times) 
		cdef int enrichment 
		if self.outfile_check(overwrite): 
			os.system("mkdir %s.vice" % (self.name)) 
			for i in range(self._mz[0].n_zones): 
				os.system("mkdir %s.vice" % (self._zones[i].name)) 

			# warn the user about r-process elements and bad solar calibrations 
			self._zones[0]._singlezone__c_version.nsns_warning() 
			self._zones[0]._singlezone__c_version.solar_z_warning() 

			# just do it #nike 
			enrichment = _multizone.multizone_evolve(self._mz) 

			# save yield settings and attributes 
			for i in range(self._mz[0].n_zones): 
				self._zones[i]._singlezone__c_version.save_yields() 
				self._zones[i]._singlezone__c_version.save_attributes() 
		else: 
			_multizone.multizone_cancel(self._mz) 
			enrichment = 0 

		self.dealign_name_attributes() 
		if enrichment == 1: 
			_multizone.multizone_cancel(self._mz) 
			raise SystemError("Internal Error") 
		elif enrichment == 2: 
			_multizone.multizone_cancel(self._mz) 
			raise RuntimeError("""Sum of migration likelihoods for at least \
zone and at least one timestep larger than 1.""") 
		elif capture: 
			return output(self.name) 
		else: 
			pass 

	def prep(self, output_times): 
		""" 
		Prepares the simulation to be ran based on the current settings. 

		Parameters 
		========== 
		output_times :: array-like 
			The array of values the user passed to run() 

		Raises 
		====== 
		Exceptions raised by subroutines 

		Notes 
		===== 
		The order of function calls here is highly sensitive to memory errors. 
		It must go setup calls, then for loop, then migration setup. Anything 
		else messes with attributes and causes values to be reset 
		""" 
		self.align_element_attributes() 
		self.zone_alignment_warnings() 
		self.timestep_alignment_error() 
		for i in range(self._mz[0].n_zones): 
			times = self._zones[i]._singlezone__zone_prep(output_times) 
			self._mz[0].zones[i][0].output_times = _cutils.copy_pylist( 
				times)
			self._mz[0].zones[i][0].n_outputs = len(times) 
		self.setup_migration()

	def outfile_check(self, overwrite): 
		""" 
		Determines if any of the output files exist and proceeds according to 
		the user specified overwrite preference. 

		Parameters 
		========== 
		overwrite :: bool 
			The user's overwrite spefication - True to force overwrite. 

		Returns 
		======= 
		True if the simulation can proceed and run, overwriting any files that 
		may already exist. False if the user wishes to abort. 
		""" 
		if overwrite: 
			if os.path.exists("%s.vice" % (self.name)): 
				os.system("rm -rf %s.vice" % (self.name)) 
			else: 
				pass 
			return True 
		else: 
			if os.path.exists("%s.vice" % (self.name)): 
				""" 
				Output directory exists. Ask the user if they'd like to wipe 
				its contents and overwrite. 
				""" 
				answer = raw_input("""\
Output directory already exists. Overwriting will delete all of its contents, \
leaving only the results of the current simulation.\nOutput directory: \
%s.vice\nOverwrite? (y | n) """ % (self.name)) 

				# be emphatic about it 
				while answer.lower() not in ["yes", "y", "no", "n"]: 
					answer = raw_input("Please enter either 'y' or 'n': ") 

				if answer.lower() in ["y", "yes"]: 
					os.system("rm -rf %s.vice" % (self.name)) 
					return True 
				else: 
					return False 
			else: 
				return True 

	def setup_migration(self): 
		""" 
		Sets up the migration matrices for simulation. Cancels the simulation 
		if there's an error. 

		Raises 
		====== 
		RuntimeError :: 
			:: 	one of the migration specifications produces a value that is 
				not between 0 and 1 at any timestep. 
		""" 
		_migration.malloc_migration_matrices(self._mz) 
		cdef long length = 10l + long(
			self._mz[0].zones[0].output_times[
				self._mz[0].zones[0].n_outputs - 1l] / 
			self._mz[0].zones[0].dt 
		) 
		eval_times = [i * self._mz[0].zones[0].dt for i in range(length)] 
		errmsg = """Migration probability must be between 0 and 1 at all \
timesteps.""" 

		for i in range(self._mz[0].n_zones): 
			for j in range(self._mz[0].n_zones): 
				""" 
				For both gas and stars, look at the i,j'th element of the 
				user-specified migration matrix. Whether it is a number or a 
				function, map it across the known evaluation times of the 
				simulation and pipe it to C 
				""" 

				# gas 
				if isinstance(self.migration.gas[i][j], numbers.Number): 
					arr = length * [self.migration.gas[i][j]] 
					if _migration.setup_migration_element(self._mz[0], 
						self._mz[0].migration_matrix_gas, 
						i, j, _cutils.copy_pylist(arr)): 

						_multizone.multizone_cancel(self._mz) 
						raise RuntimeError(errmsg) 
					else: 
						pass  
			
				elif callable(self.migration.gas[i][j]): 
					arr = list(map(self.migration.gas[i][j], eval_times)) 
					if _migration.setup_migration_element(self._mz[0], 
						self._mz[0].migration_matrix_gas, 
						i, j, _cutils.copy_pylist(arr)): 

						_multizone.multizone_cancel(self._mz) 
						raise RuntimeError(errmsg) 
					else: 
						pass  
				else: 
					raise SystemError("Internal Error") 

				# stars 
				if isinstance(self.migration.stars[i][j], numbers.Number): 
					arr = length * [self.migration.stars[i][j]] 
					if _migration.setup_migration_element(self._mz[0], 
						self._mz[0].migration_matrix_tracers, 
						i, j, _cutils.copy_pylist(arr)): 

						_multizone.multizone_cancel(self._mz) 
						raise RuntimeError(errmsg) 
					else: 
						continue 
				elif callable(self.migration.stars[i][j]): 
					arr = list(map(self.migration.stars[i][j], eval_times)) 
					if _migration.setup_migration_element(self._mz[0], 
						self._mz[0].migration_matrix_tracers, 
						i, j, _cutils.copy_pylist(arr)): 

						_multizone.multizone_cancel(self._mz) 
						raise RuntimeError(errmsg) 
					else: 
						continue 
				else: 
					raise SystemError("Internal Error") 


	def align_name_attributes(self): 
		""" 
		Checks for duplicate names within the zone attribues and raises a 
		RuntimeError if there are duplicates. Then puts the multizone object's 
		name in front of each zone's name. This ensures that the singlezone 
		objects will open files at paths of the format: 

		multizonemodel.vice/onezonemodel.vice/ 

		Checks for duplicate names as well 
		""" 
		# Start with a list of each zone's names and remove duplicates 
		names = [self._zones[i].name for i in range(self._mz[0].n_zones)] 
		names = list(dict.fromkeys(names)) 
		if len(names) < self._mz[0].n_zones: 
			raise RuntimeError("Zones with duplicate names detected.") 
		else: 
			# put multizone's name in front of each zone's name 
			for i in range(self._mz[0].n_zones): 
				self._zones[i].name = "%s.vice/%s" % (self.name, names[i]) 

	def dealign_name_attributes(self): 
		""" 
		Removes the multizone model's name from the front of each zone's name 
		at the end of a multizone simulation. 
		""" 
		for i in range(self._mz[0].n_zones): 
			self._zones[i].name = self._zones[i].name.split('/')[-1] 

	def align_element_attributes(self): 
		""" 
		Sets each zone's elements attribute to the union of all of them. 
		""" 
		# take a snapshot of each zone's elements and start w/zone 0 
		elements_attributes = [self._zones[i].elements for i in range(
			self._mz[0].n_zones)] 
		elements = list(elements_attributes[0][:]) 

		# if any zone has an element not in the list, append it 
		for i in range(1, self._mz[0].n_zones): 
			for j in elements_attributes[i]: 
				if j not in elements: 
					elements.append(j) 
				else: 
					continue 

		# Set each zone's elements to the newly determined union 
		for i in range(self._mz[0].n_zones): 
			self._zones[i].elements = elements 

	def zone_alignment_warnings(self): 
		""" 
		Raises ScienceWarnings if any of a number of attributes differ between 
		zones. 
		""" 
		n_zones = self._mz[0].n_zones 

		# attributes that shouldn't (but can) differ between zones 
		attrs = { 
			"IMF": 			[self._zones[i].IMF for i in range(n_zones)], 
			"recycling":	[self._zones[i].recycling for i in range(n_zones)], 
			"delay": 		[self._zones[i].delay for i in range(n_zones)], 
			"RIa": 			[self._zones[i].RIa for i in range(n_zones)], 
			"schmidt": 		[self._zones[i].schmidt for i in range(n_zones)], 
			"schmidt_index": [self._zones[i].schmidt_index for i in range(
				n_zones)], 
			"MgSchmidt": 	[self._zones[i].MgSchmidt for i in range(n_zones)], 
			"m_upper": 		[self._zones[i].m_upper for i in range(n_zones)], 
			"m_lower": 		[self._zones[i].m_lower for i in range(n_zones)], 
			"Z_solar": 		[self._zones[i].Z_solar for i in range(n_zones)], 
			"agb_model": 	[self._zones[i].agb_model for i in range(n_zones)] 
		} 

		def checker(key): 
			"""
			Detects any non-uniformity across zones and raises ScienceWarning 
			""" 
			if len(list(dict.fromkeys(attrs[key]))) > 1: 
				warnings.warn("""\
Attribute '%s' is not uniform across zones. This will introduce numerical \
artifacts.""" % (key), ScienceWarning)  
			else: 
				pass 

		for i in attrs.keys(): 
			checker(i) 

	def timestep_alignment_error(self): 
		""" 
		Raises a Runtime Error if the timestep size is not uniform across 
		zones. 
		""" 
		timestep_size_checker = list(dict.fromkeys(
			[self._zones[i].dt for i in range(self._mz[0].n_zones)] 
		)) 
		if len(timestep_size_checker) > 1: 
			raise RuntimeError("Timestep size not uniform across zones.") 
		else: 
			pass  

cdef class zone_array: 

	""" 
	An array of singlezone objects 
	""" 
	cdef object _zones 
	cdef int _n 

	def __init__(self, n): 
		assert isinstance(n, int), "Internal Error" 
		self._n = n 
		self._zones = n * [None] 
		for i in range(n): 
			self._zones[i] = singlezone() 
			self._zones[i].name = "zone%d" % (i) 

	def __getitem__(self, key): 
		""" 
		Allow indexing by key of type int 
		""" 
		if isinstance(key, numbers.Number): 
			if 0 <= key < self._n: 
				if key % 1 == 0: 
					return self._zones[int(key)] 
				else: 
					raise IndexError("""Index must be interpretable as an \
integer. Got: %g""" % (key)) 
			else: 
				raise IndexError("Index out of bounds: %g" % (key)) 
		else: 
			raise IndexError("Index must be an integer. Got: %s" % (type(key))) 

	def __setitem__(self, key, value): 
		""" 
		Allow indexing by key of type int; item must be of type singlezone 
		""" 
		if isinstance(key, numbers.Number): 
			if 0 <= key < self._n: 
				if key % 1 == 0: 
					if isinstance(value, singlezone): 
						self._zones[int(key)] = value 
					else: 
						raise TypeError("""Item must be of type singlezone. \
Got: %s""" % (type(value))) 
				else: 
					raise ValueError("""Index must be interpretable as an \
integer. Got: %g""" % (key)) 
			else: 
				raise ValueError("Index out of bounds: %g" % (key)) 
		else: 
			raise TypeError("Index must be an integer. Got: %s" % (type(key))) 

	def __repr__(self): 
		return str([self._zones[i] for i in range(self._n)]) 

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
		return self.exc_value is None 


cdef class migration_specifications: 

	""" 
	Migration specifications for multizone simulations. 
	""" 

	cdef object _stars 
	cdef object _gas 

	def __init__(self, n): 
		assert isinstance(n, int), "Internal Error" 
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



