# cython: language_level = 3, boundscheck = False
""" 
This file implements the yield_settings class, a subclass of the 
elemental_settings object. Instances of this object store the user's 
nucleosynthetic yields from core-collapse and type Ia supernove. 
""" 

from ...version import version as _VERSION_ 
from ..._globals import _DIRECTORY_ 
from ..._globals import _RECOGNIZED_ELEMENTS_ 
from ..._globals import _VERSION_ERROR_ 
from .. import _pyutils 
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
# from . cimport _objects 
from . cimport _yield_settings 


#------------------------- YIELD DATAFRAME SUBCLASS -------------------------#
cdef class yield_settings(elemental_settings): 

	""" 
	A subclass of the VICE dataframe which only allows keys that are the 
	symbols of elements built into VICE [case-insensitive]. Instances of this 
	class contain the user's settings for nucleosynthetic yields from various 
	astrophysical channels. These dataframes should NOT be directly assigned 
	by the user; that is, only their existing fields should be modified. 

	vice.yields.ccsne.settings 
	========================== 
	IMF-integrated yields of elements from core collapse supernovae. Settings 
	may be either numerical values or functions of time. 

	vice.yields.sneia.settings 
	========================== 
	IMF-integrated yields of elements from type Ia supernovae. Settings may be 
	numerical values only. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	# cdef object __defaults 
	# cdef object _allow_funcs 
	# cdef object _config_field 

	def __init__(self, frame, name, allow_funcs, config_field): 
		"""
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		#=====================================================================#
		"""
		(The above docstring is entered purely to keep the visible __init__ 
		docstring consistent across subclasses and instances of the VICE 
		dataframe. Below is the actual docstring for this function.)

		Parameters
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		name :: str 
			A string denoting the name of the objects stored as fields in 
			this dataframe (i.e. core-collapse yield settings.) 
		allow_funcs :: bool 
			A boolean describing whether or not functional attribute are allowed 
		config_field :: str 
			The name of the '.config' file that is stored whenever the user 
			saves new default yield settings. 
		"""
		if "settings.config" in os.listdir("%syields/%s" % (_DIRECTORY_, 
			config_field)): 
			# load settings based on saved yields 
			super().__init__(pickle.load(open("%syields/%s/settings.config" % (
				_DIRECTORY_, config_field), "rb"))) 
		else: 
			# load what was passed 
			super().__init__(frame) 
		if isinstance(name, strcomp): 
			self._name = name 
		else: 
			raise TypeError("Attribute 'name' must be of type str. Got: %s" % (
				type(name))) 

		"""
		first argument to this function will always be the factory default 
		yields. Save those as a private attribute. 
		"""
		keys = tuple([i.lower() for i in frame.keys()]) 
		fields = tuple([frame[i] for i in frame.keys()]) 
		self.__defaults = dict(zip(keys, fields)) 

		# Other private attributes 
		self._allow_funcs = allow_funcs 
		self._config_field = config_field 

	def __setitem__(self, key, value): 
		if isinstance(key, strcomp): 
			if key.lower() in _RECOGNIZED_ELEMENTS_: 
				if isinstance(value, numbers.Number): 
					# Numerical values are always allowed 
					self._frame[key.lower()] = value 
				elif callable(value): 
					# functions aren't always allowed 
					if self._allow_funcs: 
						_pyutils.args(value, """Functional %s yield settings \
must take only one numerical parameter.""" % (self._name)) 
						self._frame[key.lower()] = value 
					else:
						raise TypeError("""This dataframe does not support \
functional attributes.""") 
				else: 
					raise TypeError("""%s yield settings must be either \
numerical values or callable functions accepting one numerical parameter. \
Got: %s""" % (self._name, type(value))) 
			else: 
				raise ValueError("Unrecognized element: %s" % (key)) 
		else: 
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key))) 

	def restore_defaults(self): 
		"""
		Restores the dataframe to its default parameters. 
		"""	
		if "settings.config" in os.listdir("%syields/%s" % (_DIRECTORY_, 
			self._config_field)): 
			self._frame = pickle.load(open(
				"%syields/%s/settings.config" % (_DIRECTORY_, 
					self._config_field), "rb")) 
		else: 
			self._frame = dict(self.__defaults) 

	def factory_settings(self): 
		"""
		Restores the dataframe to its factory defaults. If user's wish to 
		revert their presets as well, simply call save_defaults() immediately 
		after. 
		""" 
		self._frame = dict(self.__defaults) 

	def save_defaults(self): 
		"""
		Saves the current dataframe settings as the default values. 

		Saving functional attributes requires dill, which is installable via 
		'pip install dill'. 
		""" 
		if "dill" in sys.modules: 
			""" 
			Regardless of the presence of callable functions, if dill is 
			imported, go ahead and save. 
			""" 
			pickle.dump(self._frame, open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "wb")) 
		elif all(map(lambda x: not callable(self._frame[x]), self.keys())): 
			# nothing is callable anyway 
			pickle.dump(self._frame, open("%syields/%s/settings.config" % (
				_DIRECTORY_, self._config_field), "wb")) 
		else: 
			raise TypeError("""\
Package 'dill' not found. At least one element is set to have a functional \
yield, and saving this requires dill (installable via pip). After installing \
dill and relaunching your python interpreter, these yields can be saved.""") 

	def remove(self, key): 
		""" 
		This function throws a TypeError whenever called. This derived class 
		of the VICE dataframe does not support item deletion. 
		""" 
		# Suppring item deletion here could break singlezone simulations 
		raise TypeError("This dataframe does not support item deletion.") 

