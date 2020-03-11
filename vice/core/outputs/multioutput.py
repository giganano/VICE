
from __future__ import absolute_import 
from ._multioutput import c_multioutput 
from . import _output_utils 
import os 

class multioutput: 

	""" 
	Reads in the output from multizone class and allows the user to access it 
	easily via VICE dataframes. The results are read in automatically. 

	Signature: vice.multioutput.__init__(name) 

	Attributes 
	========== 
	name :: str 
		The full or relative path to the output directory 
	zones :: VICE dataframe 
		A dataframe containing each zone's corresponding output object 
	tracers :: VICE dataframe 
		A dataframe containing all stellar tracer particle data 

	See Also 
	======== 
	vice.output 
	vice.history 
	vice.mdf 
	""" 

	def __new__(cls, name): 
		""" 
		__new__ is overridden such that in the event of a singlezone object, 
		an output object is returned. 
		""" 
		name = _output_utils._get_name(name) 
		if _output_utils._is_multizone(name): 
			return super(multioutput, cls).__new__(cls) 
		else: 
			from .output import output 
			return output(name) 

	def __init__(self, name): 
		""" 
		Parameters 
		========== 
		name :: str 
			The full or relative path to the output directory, with or without 
			the ".vice" extension. 

		Notes 
		===== 
		If the name of the output corresponds to that of a singlezone object, 
		an output object is returned instead of a multioutput object. 
		""" 
		self.__c_version = c_multioutput(name) 

	def __repr__(self): 
		""" 
		Prints the name of the simulation 
		""" 
		return "<VICE multioutput from multizone: %s>" % (self.name) 

	def __str__(self): 
		""" 
		Returns self.__repr__() 
		""" 
		return self.__repr__() 

	def __eq__(self, other): 
		""" 
		Returns True if both multizone output objects come from the same 
		directory 
		""" 
		if isinstance(other, multioutput): 
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
		multizone object. The ".vice" extension need not be specified with 
		the name. 
		""" 
		return self.__c_version.name 

	@property 
	def zones(self): 
		""" 
		Type :: VICE dataframe 

		The data for each simulated zone. The keys of this dataframe are the 
		names of each zone, and these map onto the associated output objects. 
		""" 
		return self.__c_version.zones 

	@property 
	def stars(self): 
		""" 
		Type :: VICE dataframe 

		The data for the tracer particles of this simulation. This stores the 
		formation time in Gyr of each particle, its mass, its formation and 
		final zone numbers, and the metallicity by mass of each element in the 
		simulation. 
		""" 
		return self.__c_version.stars   

