
from __future__ import absolute_import 
from ._output import c_output 
from . import _output_utils 
import os 

class output: 

	"""
	Reads in the output from the singlezone class and allows the user to access 
	it easily via VICE dataframes. The results are read in automatically. 

	Signature: vice.output.__init__(name)

	Attributes 
	==========
	name :: str 
		The name of the .vice directory containing the output of a singlezone 
		object. 
	elements :: tuple 
		The symbols of the elements whose enrichment was tracked by the 
		simulation. 
	history :: VICE dataframe 
		The abundances at all output times as well as the time-evolution of 
		the galaxy, such as the star formation rate, gas mass, and star 
		formation efficiency. 
	mdf :: VICE dataframe 
		The normalized stellar metallicity distribution function at the final 
		timestep of the simulation. 
	ccsne_yields :: VICE dataframe 
		The yield settings from core-collapse supernovae at the time the 
		simulation was ran. 
	sneia_yields :: VICE dataframe 
		The yield settings from type Ia supernovae at the time the simulation 
		was ran. 

	Functions 
	=========
	show :: 		Show a plot of a given quantity stored in the output 

	Notes 
	===== 
	Reinstancing functional attributes from VICE outputs requires the package 
	dill, an extension to pickle in the python standard library. It is 
	recommended that VICE users install dill if they have not already so that 
	they can make use of this feature; this can be done via 'pip install dill'. 

	VICE outputs are stored in directories with a '.vice' extension following 
	the name of the simulation assigned to the singlezone object that produced 
	it. Because the history and mdf outputs are stored in pure ascii text, this 
	allows users to open them in languages other than python while retaining 
	the ability to run <command> *.vice in a linux terminal to run operations 
	on all VICE outputs in a given directory. 

	See also 
	======== 
	vice.multioutput 
	vice.history 
	vice.mdf 
	""" 

	def __new__(cls, name): 
		""" 
		__new__ is overridden such that in the event of a multizone output, a 
		multioutput object is returned. 
		""" 
		name = _output_utils._get_name(name) 
		if _output_utils._is_multizone(name): 
			from .multioutput import multioutput 
			return multioutput(name) 
		else: 
			return super(output, cls).__new__(cls) 

	def __init__(self, name): 
		""" 
		Parameters 
		========== 
		name :: str 
			The full or relative path to the output directory, with or without 
			the ".vice" extension. 

		Notes 
		===== 
		If the name of the output corresponds to that of a multizone object, 
		a multioutput object is returned instead of an output object. 
		""" 
		self.__c_version = c_output(name) 

	def __repr__(self): 
		""" 
		Prints the name of the simulation 
		""" 
		return "<VICE output from singlezone: %s>" % (self.name) 

	def __str__(self): 
		""" 
		Returns self.__repr__() 
		""" 
		return self.__repr__() 

	def __eq__(self, other): 
		""" 
		Returns True if the outputs came from the same directory 
		""" 
		if isinstance(other, output): 
			return os.path.abspath(self.name) == os.path.abspath(other.name) 
		else: 
			return False 

	def __ne__(self, other): 
		""" 
		Returns not self.__eq__(other) 
		""" 
		return not self.__eq__(other) 

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
	def name(self): 
		"""
		Type :: str 

		The name of the ".vice" directory containing the output of a 
		singlezone object. The ".vice" extension need not be specified with 
		the name. 
		"""
		return self.__c_version.name 

	@property
	def elements(self):
		""" 
		Type :: tuple 

		The symbols for the elements whose enrichment was modeled to produce 
		the output file. 
		"""
		return self.__c_version.elements 

	@property
	def history(self):
		"""
		Type :: dataframe 

		The dataframe read in via vice.history(name). 

		See Also
		======== 
		Function vice.history
		"""
		return self.__c_version.history 

	@property
	def mdf(self):
		"""
		Type :: dataframe 

		The dataframe read in via vice.mdf(name). 

		See Also 
		======== 
		Function vice.mdf 
		"""
		return self.__c_version.mdf 

	@property 
	def agb_yields(self): 
		""" 
		Type :: dataframe 

		A dataframe encoding the settings for nucleosynthetic yields from 
		asymptotic giant branch stars at the time the simulation was ran. 

		See Also 
		======== 
		vice.yields.agb.settings 
		""" 

	@property
	def ccsne_yields(self): 
		"""
		Type :: dataframe 

		A dataframe encoding the settings for nucleosynthetic yields from 
		core collapse supernovae at the time the simulation was ran. 

		See Also 
		======== 
		vice.yields.ccsne.settings 
		"""
		return self.__c_version.ccsne_yields 

	@property
	def sneia_yields(self): 
		"""
		Type :: dataframe 

		A dataframe encoding the settings for nucleosynthetic yields from 
		type Ia supernovae at the time the simulation was ran. 

		See Also 
		======== 
		vice.yields.sneia.settings 
		"""
		return self.__c_version.sneia_yields 

	def show(self, key, xlim = None, ylim = None): 
		""" 
		Show a plot of the given quantity referenced by a keyword argument. 

		Signature: vice.output.show(key) 

		Parameters 
		========== 
		key :: str [case-insensitive] 
			The keyword argument. If this is a quantity stored in the history 
			attribute, it will be plotted against time by default. Conversely, 
			if it is stored in the mdf attribute, it will show the 
			corresponding stellar metallicity distribution function. 

			Users can also specify an argument of the format key1-key2 where 
			key1 and key2 are elements of the history output. It will then 
			plot key1 against key2 and show it to the user. 
		xlim :: array-like object containing two real numbers 
			The x-limits to impose on the shown plot 
		ylim :: array-like object containing two real numbers 
			The y-limits to impose on the shown plot 

		Raises 
		====== 
		KeyError :: 
			::	Key is not found in either history or mdf attributes 
		ImportError/ModuleNotFoundError :: 
			::	matplotlib version >= 2 is not found in the user's system. 
				(The ModuleNotFoundError is raised in python version >= 3.6.) 
		All other errors are raised by matplotlib.pyplot.show

		Notes 
		===== 
		This function is NOT intended to generate publication quality plots for 
		users. It is included purely as a convenience function for users to be 
		able to read in and immediately inspect the results of their 
		simulations in a plot with only a few lines of code. 

		Example 
		======= 
		>>> out = vice.output("example") 
		>>> out.show("dn/d[o/fe]") 
		>>> out.show("sfr") 
		>>> out.show("[o/fe]-[fe/h]") 
		"""	
		self.__c_version.show(key, xlim = xlim, ylim = ylim) 

