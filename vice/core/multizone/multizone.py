
from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ._multizone import c_multizone 
from ..outputs._output_utils import _check_singlezone_output 
from ..outputs._output_utils import _is_multizone 
from ..outputs._output_utils import _get_name 
from ..outputs import multioutput 
from ..outputs import output 
from .. import pickles 
import warnings 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

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

While the user sees the number of star particles formed per zone per timestep 
as 'n_stars', that value exists under the hood as 'n_tracers'. Star particles 
are referred to in VICE's C library as tracer particles rather than star 
particles. 
""" 

class multizone(object): 

	r""" 
	An object designed to run simulations of chemical enrichment under the 
	multi-zone approximation for user-specified parameters. At its core, this 
	is an array of ``singlezone`` objects. 

	**Signature**: vice.multizone(name = "multizonemodel", n_zones = 10, 
	n_stars = 1, simple = False, verbose = False) 

	Parameters 
	----------
	name : ``str`` [default : "multizonemodel"] 
		The attribute ``name``, initialized via keyword argument. See below. 
	n_zones : ``int`` [default : 10] 
		The attribute ``n_zones``, initialized via keyword argument. See below. 
	n_stars : ``int`` [default : 1] 
		The attribute ``n_stars``, initialized via keyword argument. See below. 
	simple : ``bool`` [default : False] 
		The attribute ``simple``, initialized via keyword argument. See below. 
	verbose : ``bool`` [default : False] 
		The attribute ``verbose``, initialized via keyword argument. See below. 

	Attributes 
	----------
	name : ``str`` [default : "multizonemodel"] 
		The name of the simulation. Output will be stored in a directory under 
		this name. 
	zones : ``zone_array`` [default : always ``singlezone`` objects] 
		An array-like object of ``singlezone`` objects, detailing the 
		evolutionary parameters of each zone. 
	migration : ``migration.specs`` [default : no migration] 
		The migration specifications for both gas and stars. 
	n_zones : ``int`` [default : 10] 
		The number of zones in the model. 
		
		.. note:: This cannot be changed after creation of the object. 

		.. note:: If this is equal to 1, a ``singlezone`` object is created 
			with the default parameters. 

	n_stars : ``int`` [default : 1] 
		The number of star particles per zone per timestep. 
	simple : ``bool`` [default : False] 
		If True, the positions of stars at intermediate times will be ignored. 
		That is, mixing is taken into account at only the final timestep. 
	verbose : ``bool`` [default : False] 
		Whether or not to print to the console as the simulation runs. 

	Functions 
	---------
	run : [instancemethod] 
		Run the simulation 
	from_output : [classmethod] 
		Obtain a ``multizone`` object with the parameters of one that produced 
		an output. 

	Example Code 
	------------
	>>> import vice 
	>>> mz = vice.multizone(n_zones = 3) 
	>>> mz
		vice.multizone{
			name -----------> multizonemodel
			n_zones --------> 3
			n_stars --------> 1
			verbose --------> False
			simple ---------> False
			zones ----------> ['zone0', 'zone1', 'zone2']
			migration ------> Stars: <function _DEFAULT_STELLAR_MIGRATION_ at 0x10e2150e0>
							  ISM:     MigrationMatrix{
			0 ---------> {0.0, 0.0, 0.0}
			1 ---------> {0.0, 0.0, 0.0}
			2 ---------> {0.0, 0.0, 0.0}
		}
		}
	""" 

	def __new__(cls, n_zones = 10, **kwargs): 
		# return a singlezone object when n_zones = 1 
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
		self.__c_version = c_multizone(n_zones = int(n_zones), **kwargs) 

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
			"n_stars": 			self.n_stars, 
			"verbose": 			self.verbose, 
			"simple": 			self.simple, 
			"zones": 			[self.zones[i].name for i in range(
									self.n_zones)], 
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

	@classmethod  
	def from_output(cls, arg): 
		r""" 
		Obtain an instance of the ``multizone`` class given either the path 
		to an output of a ``multioutput`` object itself. 

		**Signature**: vice.multizone.from_output(arg) 

		.. versionadded:: 1.1.0 

		Parameters 
		----------
		arg : ``str`` or ``multioutput`` 
			The full or relative path to the output directory; the '.vice' 
			extension is not necessary. Alternatively, an output object. 

		Returns 
		-------
		mz : ``multizone`` 
			A ``multizone`` object with the same parameters as the one which 
			produced the output. 

		Raises 
		------
		* TypeError 
			- ``arg`` is neither a ``multioutput`` object nor a string. 
		* IOError [Only occurs if the output has been altered] 
			- The output is missing files 

		Notes 
		-----
		.. note:: 

			If arg is either a ``singlezone`` output or an ``output`` object, 
			a ``singlezone`` object will be returned. 

		.. note:: 

			This function serving as the reader, the writer is the 
			vice.core.multizone._multizone.c_multizone.pickle function, 
			implemented in Cython_. 

			.. _Cython: https://cython.org/ 

		Example Code 
		------------
		>>> import numpy as np 
		>>> import vice
		>>> vice.multizone(name = "example", n_zones = 3) 
		>>> mz.run(np.linspace(0, 10, 1001)) 
		>>> mz = vice.multizone.from_output("example") 
		>>> mz 
			vice.multizone{
				name -----------> example
				n_zones --------> 3
				n_stars --------> 1
				verbose --------> False
				simple ---------> False
				zones ----------> ['zone0', 'zone1', 'zone2']
				migration ------> Stars: <function _DEFAULT_STELLAR_MIGRATION_ at 0x111393f80>
								  ISM:     MigrationMatrix{
					0 ---------> {0.0, 0.0, 0.0}
					1 ---------> {0.0, 0.0, 0.0}
					2 ---------> {0.0, 0.0, 0.0}
				}
			}
		""" 
		if isinstance(arg, multioutput): 
			# recursion to the algorithm which does it from the path 
			return cls.from_output(arg.name) 
		elif isinstance(arg, output): 
			""" 
			Return the corresponding singlezone object. 
			These import statements are here to prevent ImportErrors caused by 
			nested recursive imports. 
			""" 
			from ..singlezone import singlezone 
			return singlezone.from_output(arg) 
		elif isinstance(arg, strcomp): 
			dirname = _get_name(arg) 
			if not _is_multizone(dirname): 
				from ..singlezone import singlezone 
				return singlezone.from_output(dirname) 
		else: 
			raise TypeError("""Must be either a string or an output object. \
Got: %s""" % (type(arg))) 

		from ..singlezone import singlezone 
		attrs = pickles.jar.open("%s/attributes" % (dirname)) 
		mz = cls(n_zones = attrs["n_zones"]) 
		mz.name = attrs["name"] 
		mz.n_stars = attrs["n_stars"] 
		mz.simple = attrs["simple"] 
		mz.verbose = attrs["verbose"] 
		for i in range(mz.n_zones): 
			mz.zones[i] = singlezone.from_output("%s/%s.vice" % (dirname, 
				attrs["zones"][i])) 
			mz.zones[i].name = attrs["zones"][i] 
		
		stars = pickles.jar.open("%s/migration" % (dirname))["stars"] 
		if stars is None: 
			warnings.warn("""\
Attribute not encoded with output: migration.stars. Assuming default value, \
which may not reflect the value of this attribute at the time the simulation \
was ran.""", UserWarning) 
		else: 
			mz.migration.stars = stars 

		for i in range(mz.n_zones): 
			attrs = pickles.jar.open("%s/migration/gas%d" % (dirname, i)) 
			for j in range(mz.n_zones): 
				if attrs[str(j)] is None: 
					warnings.warn("""\
Attribute not encoded with output: migration.gas[%d][%d]. Assuming default \
value, which may not reflect the value of this attribute at the time the \
simulation was ran.""" % (i, j), UserWarning) 
				else: 
					mz.migration.gas[i][j] = attrs[str(j)]  

		return mz 


	@property 
	def name(self): 
		r""" 
		Type : ``str`` 

		Default : "multizonemodel" 

		The name of the simulation. The output will be stored in a directory 
		under this name with the extension ".vice". This can also be of the 
		form ``./path/to/directory/name`` and the output will be stored there. 

		.. tip:: 

			Users need not interact with any of the output files. The 
			``multioutput`` object is designed to read in all of the results 
			automatically. 

		.. tip:: 

			By forcing a ".vice" extension on the output directory, users can 
			run ``<command> \*.vice`` in a terminal to run commands over all 
			VICE outputs in a given directory. 

		.. note:: 

			The outputs of this class contain the output from each individual 
			zone in their respective ".vice" directories as well as the 
			abundances, age information, and initial and final zone numbers 
			of all star particles in an ascii file named "tracers.out". Like 
			the "history.out" and "mdf.out" files associated with the 
			``singlezone`` object, this allows this information to be analyzed 
			in languages other than python with ease. 

		.. seealso:: ``vice.singlezone.name`` 

		Example Code 
		------------
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> mz.name = "another_name" 
		""" 
		return self.__c_version.name 

	@name.setter 
	def name(self, value): 
		self.__c_version.name = value 

	@property 
	def zones(self): 
		r""" 
		Type : ``zone_array`` 

		Default : ``n_zones`` singlezone objects with default parameters. 

		A 1-dimensional array-like object which forces all elements to be 
		instances of the ``singlezone`` class. The attributes of each zone can 
		be manipulated in exactly the same way as other ``singlezone`` objects. 

		.. note:: 

			The output associated with each zone will be stored inside the 
			output directory from this class. For example, for a multizone 
			object whose name is "multizonemodel" with a zone named 
			"onezonemodel", the output will be stored at the path 
			``multizonemodel.vice/onezonemodel.vice``. 

		.. seealso:: ``vice.singlezone`` 

		Example Code 
		------------
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> mz.zones[0] 
			vice.singlezone{
				name -----------> zone0
				func -----------> <function _DEFAULT_FUNC_ at 0x10f896290>
				mode -----------> ifr
				verbose --------> False
				elements -------> ('fe', 'sr', 'o')
				IMF ------------> kroupa
				eta ------------> 2.5
				enhancement ----> 1.0
				entrainment ----> <entrainment settings>
				Zin ------------> 0.0
				recycling ------> continuous
				delay ----------> 0.15
				RIa ------------> plaw
				Mg0 ------------> 6000000000.0
				smoothing ------> 0.0
				tau_ia ---------> 1.5
				tau_star -------> 2.0
				schmidt --------> False
				schmidt_index --> 0.5
				MgSchmidt ------> 6000000000.0
				dt -------------> 0.01
				m_upper --------> 100.0
				m_lower --------> 0.08
				postMS ---------> 0.1
				Z_solar --------> 0.014
				bins -----------> [-3, -2.95, -2.9, ... , 0.9, 0.95, 1]
			}
		""" 
		return self.__c_version.zones 

	@property 
	def migration(self): 
		r""" 
		Type : ``migration.specs`` 

		Default : No migration of either gas or stars. 

		An object which stores the migration specifications of the multizone 
		model. 

		Attributes 
		----------
		gas : ``mig_matrix`` 
			A matrix describing how gas moves between zones. 
		stars : <function> 
			The migration settings for star particles. 

		.. seealso:: 

			- ``vice.multizone.migration.gas`` 
			- ``vice.multizone.migration.stars`` 

		Example Code 
		------------
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> mz.migration.gas[1][0] = 0.05 
		>>> mz.migration.gas[0][1] = 0.05 
		>>> def f(zone, tform, time): 
			'''
			stars born in zone 0 and 1 swap positions when they're more 
			than 1 Gyr old. 
			''' 
			if zone == 0: 
				if time - tform > 1: 
					return 1 
				else: 
					return 0 
			elif zone == 1: 
				if time - tform > 1: 
					return 0 
				else: 
					return 1 
			else: 
				return zone 
		>>> mz.migration.stars = f 
		""" 
		return self.__c_version.migration 

	@migration.setter 
	def migration(self, value): 
		self.__c_version.migration = value 

	@property 
	def n_zones(self): 
		r""" 
		Type : ``int`` 

		Default : 10 

		The number of zones in the simulation. 

		.. note:: 

			This value may only be set upon initialization of the ``multizone`` 
			object. In order to change the number of zones in the model, a 
			new ``multizone`` object must be created. 

		Example Code 
		------------
		>>> import vice
		>>> mz1 = vice.multizone(name = "example1", n_zones = 8) 
		>>> mz2 = vice.multizone(name = "example2", n_zones = 12) 
		>>> mz2.n_zones 
			12 
		""" 
		return self.__c_version.n_zones 

	@property 
	def n_stars(self): 
		r""" 
		Type : ``int`` 

		Default : 1 

		The number of star particles to form per zone per timestep. These are 
		tracer particles which are stand-ins for entire stellar populations 
		which form and migrate between zones according to the attribute 
		``migration.stars``. 

		.. note:: If the star formation rate varies in the simulation, this 
			will impact the simulation by forming star particles of different 
			masses as opposed to a different number of star particles. 

		Example Code 
		------------
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> mz.n_stars 
			1 
		>>> mz.n_stars = 3 
		>>> mz.n_stars 
			3 
		""" 
		return self.__c_version.n_tracers 

	@n_stars.setter 
	def n_stars(self, value): 
		self.__c_version.n_tracers = value 

	@property 
	def verbose(self): 
		r""" 
		Type : ``bool`` 

		Default : ``False`` 

		If True, the simulation will print to the console as it evolves. 

		Example Code 
		------------
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> mz.verbose = True 
		""" 
		return self.__c_version.verbose 

	@verbose.setter 
	def verbose(self, value): 
		self.__c_version.verbose = value 

	@property 
	def simple(self): 
		r""" 
		Type : ``bool`` 

		Default : ``False`` 

		If ``True``, the star particles' zone numbers at timestep between 
		formation and the final timestep will be ignored. Each zone will 
		evolve independently, and mixing will be accounted for only at the 
		final timestep. If ``False``, this information will be taken into 
		account as the simulation evolves. 

		.. warning:: Johnson et al. (2020, in prep) argues that the positions 
			of stars as they migrate is necessary information to accurately 
			model galactic chemical evolution. This suggests that this 
			attribute should be always be ``False``. 

		Raises 
		------
		* ScienceWarning 
			- This attribute is set to ``True``. 

		Example Code 
		------------
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> mz.simple 
			False 
		""" 
		return self.__c_version.simple 

	@simple.setter 
	def simple(self, value): 
		self.__c_version.simple = value 

	def run(self, output_times, capture = False, overwrite = False): 
		r""" 
		Run the simulation. 

		**Signature**: x.run(output_times, capture = False, overwrite = False) 

		Parameters 
		----------
		x : ``multizone`` 
			An instance of this class. 
		output_times : array-like [elements are real numbers] 
			The times in Gyr at which VICE should record output from the 
			simulation. These need not be sorted from least to greatest. 
		capture : ``bool`` [default : False] 
			If ``True``, an output object containing the results of the 
			simulation will be returned. 
		overwrite : ``bool`` [default : False] 
			If ``True``, will force overwrite any files with the same name as 
			the simulation output files. 

		Returns 
		-------
		out : ``multioutput`` [only returned if ``capture == True``] 
			A ``multioutput`` object produced from this simulation's output. 

		Raises 
		------
		* RuntimeError 
			- 	A migration matrix cannot be setup properly according to the 
				current specifications. 
			- 	Any of the zones have duplicate names. 
			- 	The timestep size is not uniform across all zones. 
		* ScienceWarning 
			-	Any of the attributes ``IMF``, ``recycling``, ``delay``, 
				``RIa``, ``schmidt``, ``schmidt_index``, ``MgSchmidt``, 
				``m_upper``, ``m_lower``, or ``Z_solar`` aren't uniform across 
				all zones. Realistically these attributes would be, but this 
				is not required for the simulation to run properly. 

		Other exceptions are raised by ``vice.singlezone.run``. 

		Notes 
		-----
		.. note:: 

			Calling this function only causes VICE to produce the output files. 
			The ``multioutput`` class handles the reading and storing of the 
			simulation results. 

		.. note:: 

			Saving functional attributes with VICE outputs requires the 
			package dill_, an extension to ``pickle`` in the python standard 
			library. It is recommended that VICE users install dill_ >= 0.2.0. 

			.. _dill: https://pypi.org/project/dill/ 

		.. note:: 

			When ``overwrite == False``, and there are files under the same 
			name as the output produced, this acts as a halting function. VICE 
			will wait for the user's approval to overwrite existing files in 
			this case. If users are running multiple simulations and need 
			their integrations not to stall, they must specify 
			``overwrite = True``. 

		Example Code 
		------------
		>>> import numpy as np 
		>>> import vice 
		>>> mz = vice.multizone(name = "example") 
		>>> outtimes = np.linspace(0, 10, 1001) 
		>>> mz.run(outtimes) 
		""" 
		return self.__c_version.run(output_times, capture = capture, 
			overwrite = overwrite) 

