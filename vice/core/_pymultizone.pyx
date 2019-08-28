# cython: language_level = 3, boundscheck = False
""" 
This file implements the python wrapper of the multizone object, which runs 
simulations under the singlezone approximation. Most of the subroutins are in 
C, found in the vice/src/ directory within the root tree. 
""" 

# Python imports 
from __future__ import absolute_import, division 
from .._globals import _DEFAULT_TRACER_MIGRATION_ 
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
	input = raw_input 
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
from . cimport _stats 
from . cimport _tracer 

""" 
NOTES 
===== 
cdef class objects do not transfer the docstrings of class attributes to the 
compiled output, leaving out the internal documentation. For this reason, 
wrapping of the multizone object has two layers -> a python class and a 
C class. In the python class, there is only one attribute: the C version of 
the wrapper. The docstrings are written here, and each function/setter 
only calls the C version of the wrapper. While this is a more complicated 
wrapper, it preserves the internal documentation. In order to maximize 
readability, the setter functions of the C version of the wrapper have brief 
notes on the physical interpretation of each attribute as well as the allowed 
types and values. 
""" 

class multizone(object): 

	""" 
	Runs simulations of chemical enrichment under the multi-zone approximation 
	for user-specified parameters. 

	Signature vice.multizone.__init__(name = "multizonemodel", 
		n_zones = 10, 
		n_tracers = 1, 
		verbose = False) 

	Attributes 
	========== 
	name :: str [default :: "multizonemodel"] 
		The name of the simulation 
	n_zones :: int [default :: 10] 
		The number of zones in the simulation 
	n_tracers :: int [default :: 1] 
		The number of tracer particles per zone per timestep 
	verbose :: bool [default :: False] 
		Whether or not to print the time to the console as the simulation runs 
	migration :: object [default :: zeroes] 
		The migration matrices specifying how gas and stellar tracer particles 
		should be moved between zones at each timestep. 

	Functions 
	========= 
	run :: 
		Run the simulation 

	See also 	[https://github.com/giganano/VICE/tree/master/docs] 
	======== 
	VICE's science documentation 
	""" 

	def __new__(cls, n_zones = 10, **kwargs): 
		""" 
		__new__ is overridden such that a singlezone object is returned 
		when n_zones = 1. 
		""" 
		if isinstance(n_zones, numbers.Number): 
			if n_zones > 0: 
				if n_zones % 1 == 0: 
					n_zones = int(n_zones) 
					if n_zones == 1: 
						return singlezone() 
					else: 
						return super(multizone, cls).__new__(cls) 
				else: 
					raise ValueError("""Attribute 'n_zones' must be of type \
int. Got: %g""" % (n_zones)) 
			else: 
				raise ValueError("Attribute 'n_zones' must be non-negative.") 
		else: 
			raise TypeError("""Attribute 'n_zones' must be of type int. \
Got: %s""" % (type(n_zones))) 

	def __init__(self, n_zones = 10, **kwargs): 
		""" 
		All attributes can be specified as a keyword argument. 

		Notes 
		===== 
		When n_zones = 1, a singlezone object is initialized 
		""" 
		self.__c_version = c_multizone(n_zones = int(n_zones), **kwargs) 

	def __repr__(self): 
		return self.__c_version.__repr__() 

	def __str__(self): 
		return self.__c_version.__str__() 

	def __enter__(self): 
		""" 
		Opens a with statement 
		""" 
		return self.__c_version.__enter__() 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions inside with statements 
		""" 
		return self.__c_version.__exit__(exc_type, exc_value, exc_tb)  

	@property 
	def name(self): 
		""" 
		Type :: str 
		Default :: "multizonemodel" 

		The name of the simulation. The output will be stored in a directory 
		under this name with the extension ".vice". This can also be of the 
		form /path/to/directory/name and the output will be stored there. 

		Notes 
		===== 
		The user need not interact with any of the output files; the output 
		object is designed to read in all of the results automatically. 

		By forcing a ".vice" extension on the output file, users can run 
		'<command> *.vice' in a linux terminal to run commands over all VICE 
		outputs in a given directory. 

		See Also 
		======== 
		vice.singlezone 
		vice.singlezone.name 
		""" 
		return self.__c_version.name 

	@name.setter 
	def name(self, value): 
		self.__c_version.name = value 

	@property 
	def zones(self): 
		""" 
		Type :: array-like 
		
		An array-like object whose elements are the singlezone objects 
		corresponding to each individual zone in the simulation. Since the 
		elements of this property are all singlezone objects, their attributes 
		and output may all be manipulated as such. 

		Notes 
		===== 
		The output associated with each zone will be stored inside the output 
		directory from this class. For example, for a multizone object whose 
		name is "multizonemodel" with a zone named "onezonemodel", the output 
		will be stored in the path: 

		multizonemodel.vice/onezonemodel.vice 

		See Also 
		======== 
		vice.singlezone 
		vice.singlezone.name 
		""" 
		return self.__c_version.zones 

	@property 
	def migration(self): 
		""" 
		Type :: object 

		The migration specifications of the multizone model. For a simulation 
		with N zones, the migration matrix is NxN, where the ij'th element 
		represents the likelihood that either gas or stars migrate OUT OF the 
		i'th zone and INTO the j'th zone. 

		Attributes 
		========== 
		stars :: object 
			The migration matrix for tracer particles of stellar populations 
		gas :: object 
			The migration matrix for interstellar gas 

		Notes 
		===== 
		By default, both migration matrices have elements that default to 
		zero, meaning that by default this object runs N singlezone simulations 
		with stars and gas that never migrate between zones. It is up to the 
		user to specify each individual likelihood. 
		""" 
		return self.__c_version.migration 

	@property 
	def n_zones(self): 
		""" 
		Type :: int 
		Default :: 10 

		The number of zones in the simulation. 

		Notes 
		===== 
		Users may only manipulate the value of thie object upon initialization 
		of the multizone object. In order to change the number of zones in a 
		multizone simulation, a new multizone object must be initialized. 
		""" 
		return self.__c_version.n_zones 

	@property 
	def n_tracers(self): 
		""" 
		Type :: int 
		Default :: 1 

		The number of tracer particles per zone per timestep. These tracer 
		particles represent the stellar populations that form in each zone, 
		and migrate between zones according to the user-specified migration 
		matrix. 
		""" 
		return self.__c_version.n_tracers 

	@n_tracers.setter 
	def n_tracers(self, value): 
		self.__c_version.n_tracers = value 

	@property 
	def verbose(self): 
		""" 
		Type :: bool 
		Default :: False 

		If True, the time in Gyr will print to the console as the simulation 
		evolves. 
		""" 
		return self.__c_version.verbose 

	@verbose.setter 
	def verbose(self, value): 
		self.__c_version.verbose = value 

	@property 
	def simple(self): 
		""" 
		Type :: bool 
		Default :: True 

		If False, the tracer particles' zone numbers at each intermediate 
		timestep will be taken into account. Otherwise, each zone will 
		evolve independently of one another, and the metallicity distribution 
		functions will be computed from the final positions of each tracer 
		particle. 
		""" 
		return self.__c_version.simple 

	@simple.setter 
	def simple(self, value): 
		self.__c_version.simple = value 

	def run(self, output_times, capture = False, overwrite = False): 
		""" 
		Run's the built-in timestep integration routines over the parameters 
		built into the attributes of this class as well as the individual 
		zones associated with it. Whether or not the user sets capture = True, 
		the output files will be produced and can be read into an output 
		object at any time. 

		Signature: vice.multizone.run(output_times, capture = False, 
			overwrite = False) 

		Parameters 
		========== 
		output_times :: array-like [elements are real numbers] 
			The time in Gyr at which VICE should record output from the 
			simulation. These need not be sorted in any way; VICE will take 
			care of that automatically. 
		capture :: bool [default :: False] 
			A boolean describing whether or not to return an output object 
			from the results of the simulation. 
		overwrite :: bool [default :: False] 
			A boolean describing whether or not to force overwrite any 
			existing files under the same name as this simulation. 

		Returns 
		======= 
		out :: vice.dataframe [only returned if capture = True] 
			A VICE dataframe relating each zone to its associated output 
			object. 

		Raises 
		====== 
		RuntimeError :: 
			::	A migration matrix cannot be setup properly according to the 
				user's current specifications 
			::	Any of the zones associated with this object have duplicate 
				names 
			:: 	The timestep size is not uniform across each zone 
		ScienceWarning :: 
			::	Any of the attributes 'IMF', 'recycling', 'delay', 'RIa', 
				'schmidt', 'schmidt_index', 'MgSchmidt', 'm_upper', 'm_lower', 
				'Z_solar', and 'agb_model' aren't uniform across all zones. 
				Realistically these attributes would be, but this is not 
				required for the simulation to run properly. 
		Other exceptions raised by vice.singlezone.run 

		Notes
		=====
		Encoding functional attributes into VICE outputs requires the 
		package dill, an extension to pickle in the python standard library. 
		Without this, the outputs will not have memory of any functional 
		attributes stored in this class. It is recommended that VICE users 
		install dill if they have not already so that they can make use of this 
		feature; this can be done via 'pip install dill'. 

		When overwrite = False, and there are files under the same name as the 
		output produced, this acts as a halting function. VICE will wait for 
		the user's approval to overwrite existing files in this case. If 
		user's are running multiple simulations and need their integrations 
		not to stall, they must specify overwrite = True. 

		Example 
		======= 
		>>> import numpy as np 
		>>> mz = vice.multizone(name = "example") 
		>>> outtimes = np.linspace(0, 10, 1001) 
		>>> mz.run(outtimes) 
		""" 
		return self.__c_version.run(output_times, capture = capture, 
			overwrite = overwrite) 


cdef class c_multizone: 

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
		simple = True, 
		verbose = False): 

		assert isinstance(n_zones, int), "Internal Error" 
		assert n_zones > 0, "Internal Error" 
		self._mz = _multizone.multizone_initialize(n_zones) 
		self._zones = zone_array(n_zones) 
		for i in range(n_zones): 
			_multizone.link_zone(
				self._mz, 
				self._zones[i]._singlezone__zone_object_address(), 
				i) 


	def __init__(self, 
		n_zones = 10, 
		name = "multizonemodel", 
		n_tracers = 1, 
		simple = True, 
		verbose = False): 

		assert isinstance(n_zones, int), "Internal Error" 
		assert n_zones > 0, "Internal Error" 
		self.name = name 
		self._migration = migration_specifications(n_zones) 
		self.n_tracers = n_tracers 
		self.simple = simple 
		self.verbose = verbose 


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
			"simple": 			self.simple, 
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
		return self._mz[0].mig[0].n_zones 

	@property 
	def n_tracers(self): 
		# docstring in python version 
		return self._mz[0].mig[0].n_tracers 

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
					self._mz[0].mig[0].n_tracers = <unsigned int> value 
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
	def simple(self): 
		# docstring in python version 
		return bool(self._mz[0].simple) 

	@simple.setter 
	def simple(self, value): 
		""" 
		Whether or not to forget about the migration histories of the tracer 
		particles. If this value is False, they're zone number at each 
		timestep will be taken into account 

		Allowed Types 
		============= 
		bool 

		Allowed Values 
		============== 
		True and False 
		""" 
		if isinstance(value, numbers.Number) or isinstance(value, bool): 
			if value: 
				self._mz[0].simple = 1 
			else: 
				self._mz[0].simple = 0 
		else: 
			raise TypeError("""Attribute 'simple' must be interpretable as \
a boolean. Got: %s""" % (type(value))) 

	@property 
	def migration(self): 
		# docstring in python version 
		return self._migration 

	def run(self, output_times, capture = False, overwrite = False): 
		self.align_name_attributes() 
		self.prep(output_times) 
		cdef int enrichment 
		if self.outfile_check(overwrite): 
			os.system("mkdir %s.vice" % (self.name)) 
			for i in range(self._mz[0].mig[0].n_zones): 
				os.system("mkdir %s.vice" % (self._zones[i].name)) 
			self.setup_migration() # used to be in self.prep

			# warn the user about r-process elements and bad solar calibrations 
			self._zones[0]._singlezone__c_version.nsns_warning() 
			self._zones[0]._singlezone__c_version.solar_z_warning() 

			# just do it #nike 
			enrichment = _multizone.multizone_evolve(self._mz) 
			self.save_zone_numbers() 
			self.save_attributes() 

			# save yield settings and attributes 
			for i in range(self._mz[0].mig[0].n_zones): 
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
		elif enrichment == 3: 
			raise IOError("Couldn't save tracer particle data.") 
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
		for i in range(self._mz[0].mig[0].n_zones): 
			times = self._zones[i]._singlezone__zone_prep(output_times) 
			self._mz[0].zones[i][0].output_times = _cutils.copy_pylist( 
				times)
			self._mz[0].zones[i][0].n_outputs = len(times) 
		# setup migration moved to after the outfile check 
		# self.setup_migration() 

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
				answer = input("""\
Output directory already exists. Overwriting will delete all of its contents, \
leaving only the results of the current simulation.\nOutput directory: \
%s.vice\nOverwrite? (y | n) """ % (self.name)) 

				# be emphatic about it 
				while answer.lower() not in ["yes", "y", "no", "n"]: 
					answer = input("Please enter either 'y' or 'n': ") 

				if answer.lower() in ["y", "yes"]: 
					os.system("rm -rf %s.vice" % (self.name)) 
					return True 
				else: 
					return False 
			else: 
				return True 

	def setup_migration(self): 
		""" 
		Sets up both the gas and stellar migration for simulation 
		""" 
		self.setup_gas_migration() 
		self.setup_tracers() 

	def setup_gas_migration(self): 
		""" 
		Sets up the gas migration matrix for simulation. Cancels the simulation 
		if there's an error. 

		Raises 
		====== 
		RuntimeError :: 
			:: 	one of the migration specifications produces a value that is 
				not between 0 and 1 at any timestep. 
		""" 
		_migration.malloc_gas_migration(self._mz) 
		cdef long length = 10l + long(
			self._mz[0].zones[0].output_times[
				self._mz[0].zones[0].n_outputs - 1l] / 
			self._mz[0].zones[0].dt 
		) 
		eval_times = [i * self._mz[0].zones[0].dt for i in range(length)] 
		errmsg = """Migration probability must be between 0 and 1 at all \
timesteps.""" 

		for i in range(self._mz[0].mig[0].n_zones): 
			for j in range(self._mz[0].mig[0].n_zones): 
				""" 
				For both gas and stars, look at the i,j'th element of the 
				user-specified migration matrix. Whether it is a number or a 
				function, map it across the known evaluation times of the 
				simulation and pipe it to C 

				Notes 
				===== 
				Don't ignore i == j. In this case under-the-hood the migration 
				matrix will ALWAYS be zero. 
				""" 

				# gas 
				if isinstance(self.migration.gas[i][j], numbers.Number): 
					arr = length * [self.migration.gas[i][j]] 
					if _migration.setup_migration_element(self._mz[0], 
						self._mz[0].mig[0].gas_migration, 
						i, j, _cutils.copy_pylist(arr)): 

						_multizone.multizone_cancel(self._mz) 
						raise RuntimeError(errmsg) 
					else: 
						pass  
			
				elif callable(self.migration.gas[i][j]): 
					arr = list(map(self.migration.gas[i][j], eval_times)) 
					if _migration.setup_migration_element(self._mz[0], 
						self._mz[0].mig[0].gas_migration, 
						i, j, _cutils.copy_pylist(arr)): 

						_multizone.multizone_cancel(self._mz) 
						raise RuntimeError(errmsg) 
					else: 
						pass  
				else: 
					raise SystemError("Internal Error") 

				# stars 
				# if isinstance(self.migration.stars[i][j], numbers.Number): 
				# 	arr = length * [self.migration.stars[i][j]] 
				# 	if _migration.setup_migration_element(self._mz[0], 
				# 		self._mz[0].migration_matrix_tracers, 
				# 		i, j, _cutils.copy_pylist(arr)): 

				# 		_multizone.multizone_cancel(self._mz) 
				# 		raise RuntimeError(errmsg) 
				# 	else: 
				# 		continue 
				# elif callable(self.migration.stars[i][j]): 
				# 	arr = list(map(self.migration.stars[i][j], eval_times)) 
				# 	if _migration.setup_migration_element(self._mz[0], 
				# 		self._mz[0].migration_matrix_tracers, 
				# 		i, j, _cutils.copy_pylist(arr)): 

				# 		_multizone.multizone_cancel(self._mz) 
				# 		raise RuntimeError(errmsg) 
				# 	else: 
				# 		continue 
				# else: 
				# 	raise SystemError("Internal Error") 

	def setup_tracers(self): 
		bins = _pyutils.range_(-0.05, self.n_zones + 1 - 0.05, 0.05) 
		cdef double *zone_bins = _cutils.copy_pylist(bins)
		cdef double *zone_sample 
		cdef double *zone_dist 
		_tracer.malloc_tracers(self._mz) 
		n = _singlezone.n_timesteps(self._mz[0].zones[0][0]) 
		x = 0
		for i in range(n): 
			for j in range(self.n_zones): 
				# The distribution specified at this zone and timestep 
				zone_dist = _cutils.copy_pylist(
					list(map(self.migration.stars(j, 
						i * self._mz[0].zones[0][0].dt), 
					bins)))  
				zone_sample = _stats.sample( 
					zone_dist, 
					zone_bins, 
					len(bins) - 1l, 
					self.n_tracers) 
				free(zone_dist) 
				if zone_sample is not NULL: 
					for k in range(self.n_tracers): 
						if _tracer.setup_zone_history(
							self._mz[0], 
							self._mz[0].mig[0].tracers[x], 
							<unsigned long> j, 
							<unsigned long> zone_sample[k], 
							<unsigned long> i): 
							raise SystemError("Internal Error") 
						else: 
							x += 1
							continue 
					free(zone_sample) 
				else: 
					raise RuntimeError("""\
Could not sample from distribution at time t = %g and initial zone number = \
%d. Please ensure that the specified stellar migration prescription does not \
exhibit any numerical delta functions.""" % (
						i * self._mz[0].zones[0][0].dt, j))
			if self.verbose: 
				sys.stdout.write("""Setting up tracer particles. Progress: \
%.1f%%\r""" % (100 * (i + 1) / n)) 
				sys.stdout.flush() 
			else: 
				pass 
		if self.verbose: sys.stdout.write("\n") 

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
		names = [self._zones[i].name for i in range(self._mz[0].mig[0].n_zones)] 
		names = list(dict.fromkeys(names)) 
		if len(names) < self._mz[0].mig[0].n_zones: 
			raise RuntimeError("Zones with duplicate names detected.") 
		else: 
			# put multizone's name in front of each zone's name 
			for i in range(self._mz[0].mig[0].n_zones): 
				self._zones[i].name = "%s.vice/%s" % (self.name, names[i]) 

	def dealign_name_attributes(self): 
		""" 
		Removes the multizone model's name from the front of each zone's name 
		at the end of a multizone simulation. 
		""" 
		for i in range(self._mz[0].mig[0].n_zones): 
			self._zones[i].name = self._zones[i].name.split('/')[-1] 

	def align_element_attributes(self): 
		""" 
		Sets each zone's elements attribute to the union of all of them. 
		""" 
		# take a snapshot of each zone's elements and start w/zone 0 
		elements_attributes = [self._zones[i].elements for i in range(
			self._mz[0].mig[0].n_zones)] 
		elements = list(elements_attributes[0][:]) 

		# if any zone has an element not in the list, append it 
		for i in range(1, self._mz[0].mig[0].n_zones): 
			for j in elements_attributes[i]: 
				if j not in elements: 
					elements.append(j) 
				else: 
					continue 

		# Set each zone's elements to the newly determined union 
		for i in range(self._mz[0].mig[0].n_zones): 
			self._zones[i].elements = elements 

	def zone_alignment_warnings(self): 
		""" 
		Raises ScienceWarnings if any of a number of attributes differ between 
		zones. 
		""" 
		n_zones = self._mz[0].mig[0].n_zones 

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
			[self._zones[i].dt for i in range(self._mz[0].mig[0].n_zones)] 
		)) 
		if len(timestep_size_checker) > 1: 
			raise RuntimeError("Timestep size not uniform across zones.") 
		else: 
			pass 

	def save_zone_numbers(self): 
		""" 
		Saves a dictionary of zone indeces to zone names once the simulation 
		has ran for mirroring purposes. 
		""" 
		# splitting on '/' removes multizone name from each zone 
		zone_numbers = dict(zip(
			list(range(self.n_zones)), 
			[self.zones[i].name.split('/')[-1] for i in range(self.n_zones)]
		)) 
		pickle.dump(
			zone_numbers, 
			open("%s.vice/zone_numbers.config" % (self.name), "wb"
		)) 

	def save_attributes(self): 
		""" 
		Saves the multizone parameters to the output file 
		""" 
		params = {
			"name": 			self.name, 
			"n_zones": 			self.n_zones, 
			"n_tracers": 		self.n_tracers, 
			"simple": 			self.simple, 
			"verbose": 			self.verbose 
		} 
		if "dill" in sys.modules: 
			params["migration.gas"] = self.migration.gas 
			params["migration.stars"] = self.migration.stars 
		else: 
			""" 
			User doesn't have dill. Switch functional elements of migration 
			matrices to 0.0 
			""" 
			# gas, stars = self.copy_migration_matrices() 
			params["migration.gas"] = self.copy_gas_migration() 
			params["migration.stars"] = None 
		pickle.dump(params, open("%s.vice/params.config" % (self.name), "wb")) 

	def copy_gas_migration(self): 
		warn = False 
		gas = migration_matrix(self.n_zones) 
		for i in range(self.n_zones): 
			for j in range(self.n_zones): 
				if callable(self.migration.gas[i][j]): 
					warn = True 
					gas[i][j] = 0.0 
				else: 
					gas[i][j] = self.migration.gas[i][j] 
		if warn: 
			warnings.warn("""\
Saving functional attributes within VICE outputs requires dill (installable \
via pip). The functional elements of the gas migration matrix will not be \
saved with this output""", ScienceWarning) 
		else: 
			pass 

		return gas  

# 	def copy_migration_matrices(self): 
# 		warn = False 
# 		gas = migration_matrix(self.n_zones) 
# 		stars = migration_matrix(self.n_zones) 
# 		for i in range(self.n_zones): 
# 			for j in range(self.n_zones): 
# 				if callable(self.migration.gas[i][j]): 
# 					warn = True 
# 					gas[i][j] = 0.0 
# 				else: 
# 					gas[i][j] = self.migration.gas[i][j] 
# 				if callable(self.migration.stars[i][j]): 
# 					warn = True 
# 					stars[i][j] = 0.0 
# 				else: 
# 					stars[i][j] = self.migration.stars[i][j] 

# 		if warn: 
# 			warnings.warn("""\
# Saving functional attributes within VICE outputs requires dill (installable \
# via pip). The functional elements of these migration matrices will not be \
# saved with this output.""", ScienceWarning) 
# 		else: 
# 			pass  

# 		return [gas, stars] 

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
						""" 
						Because the memory addresses of each singlezone object 
						is copied into the multizone object, must instead copy 
						each attribute here, preventing memory errors 
						""" 
						self.__copy_attributes(int(key), value) 
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

	def __copy_attributes(self, key, sz): 
		""" 
		Copies the attributes of singlezone object sz into the zone at index 
		key 
		""" 
		assert isinstance(key, int), "Internal Error" 
		assert isinstance(sz, singlezone), "Internal Error" 
		self._zones[int(key)].agb_model 		= sz.agb_model
		self._zones[int(key)].bins 				= sz.bins
		self._zones[int(key)].delay 			= sz.delay
		self._zones[int(key)].dt 				= sz.dt
		self._zones[int(key)].RIa 				= sz.RIa
		self._zones[int(key)].elements 			= sz.elements
		self._zones[int(key)].enhancement 		= sz.enhancement
		self._zones[int(key)].eta 				= sz.eta
		self._zones[int(key)].func 				= sz.func
		self._zones[int(key)].IMF 				= sz.IMF
		self._zones[int(key)].m_lower 			= sz.m_lower
		self._zones[int(key)].m_upper 			= sz.m_upper
		self._zones[int(key)].Mg0 				= sz.Mg0
		self._zones[int(key)].MgSchmidt 		= sz.MgSchmidt
		self._zones[int(key)].mode 				= sz.mode
		self._zones[int(key)].name 				= sz.name
		self._zones[int(key)].recycling 		= sz.recycling
		self._zones[int(key)].schmidt 			= sz.schmidt
		self._zones[int(key)].schmidt_index 	= sz.schmidt_index
		self._zones[int(key)].smoothing 		= sz.smoothing
		self._zones[int(key)].tau_ia 			= sz.tau_ia
		self._zones[int(key)].tau_star 			= sz.tau_star
		self._zones[int(key)].Z_solar 			= sz.Z_solar
		self._zones[int(key)].Zin 				= sz.Zin


cdef class migration_specifications: 

	""" 
	Migration specifications for multizone simulations. 
	""" 

	cdef object _stars 
	cdef object _gas 

	def __init__(self, n): 
		assert isinstance(n, int), "Internal Error" 
		self.stars = _DEFAULT_TRACER_MIGRATION_ 
		self._gas = migration_matrix(n) 

	def __repr__(self): 
		rep = "Stars: %s\n" % (str(self._stars)) 
		for i in range(22): 
			rep += ' '
		rep += "ISM: " 
		for i in str(self._gas).split('\n'): 
			rep += "    %s\n" % (i) 
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
		TO the j'th zone in the simulation during a 10 Myr time interval. 
		These entries may be either numerical values or functions of time in 
		Gyr. In all cases, the value at a given time must be between 0 and 1, 
		because the elements are interpreted as likelihoods. 
		""" 
		return self._gas 

	@property 
	def stars(self): 
		""" 
		The migration settings associated with the stellar tracer particles. 

		This must be a callable object accepting two numerical parameters 
		which returns a callable object accepting one numerical parameter, and 
		is interpreted as a function of zone number and time returning the 
		distribution of final zone numbers. 
		""" 
		return self._stars 

	@stars.setter 
	def stars(self, value): 
		if callable(value): 
			try: 
				x = value(0, 0) 
			except TypeError: 
				raise ValueError("""Stellar migration setting must accept \
two numerical parameters.""") 
			if callable(x): 
				try: 
					x(0) 
				except TypeError: 
					raise ValueError("""Stellar migration setting must return \
an object accepting one numerical parameter.""") 
				self._stars = value 
			else: 
				raise TypeError("""Stellar migration setting must return a \
callable object.""") 
		else: 
			raise TypeError("""Stellar migration setting must be a callable \
object.""") 


