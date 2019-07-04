# cython: language_level = 3, boundscheck = False
"""
This file handles the implementation of the VICE dataframe. 
""" 

from __future__ import absolute_import 
from .._globals import _DIRECTORY_ 
from .._globals import _RECOGNIZED_ELEMENTS_ 
from .._globals import _VERSION_ERROR_ 
from .._globals import ScienceWarning 
from . import _pyutils 
import math as m 
import warnings 
import numbers 
import pickle 
import atexit 
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

from libc.stdlib cimport malloc, realloc, free 
from . cimport _io 

#------------------------- VICE DATAFRAME BASE CLASS -------------------------#
cdef class base: 

	"""
                                 The VICE Dataframe 
	==========================================================================
	Provides a means of storing data indexed by strings in a case-insensitive 
	manner. VICE includes several instances of this class at the global level, 
	some of which have features specific to their instance. Users may call 
	these dataframes as a function using parentheses rather than square 
	brackets and it will return the same thing. If a dataframe stores 
	array-like attributes, it may also be indexed via an integer to pull that 
	element from each field. 

	Signature: vice.dataframe.__init__(frame) 

	Functions
	=========
	keys		
	todict

	Yield Setting Dataframes 
	======================== 
	The following dataframes store the user's settings for nucleosynthetic 
	yields from core collapse and type Ia supernovae. In the case of 
	core collapse supernovae yields, the user may specify a function 
	accepting one numerical parameter, which will be interpreted as the 
	metallicity by mass Z of the stellar population. 

	yields.ccsne.settings :: Yield settings from core collapse supernovae 
	yields.sneia.settings :: Yield settings from type Ia supernovae 

	Functions Associated with these Dataframes 
	------------------------------------------ 
	factory_defaults :: Revert to VICE's original defaults 
	restore_defaults :: Revert to user's specified defaults 
	save_defaults :: Save current settings as defaults 

	Other Built-in dataframes 
	========================= 
	VICE provides the following dataframes. 

	atomic_number
	------------- 
	Stores the number of protons in the nucleus of each of VICE's recognized 
	elements. By design, this dataframe does not support item assignment 

	solar_z 
	-------  
	Stores the abundance by mass of elements in the sun. By nature, this 
	dataframe does not support user customization. Solar abundances are 
	derived from Asplund et al. (2009) and have been converted to a mass 
	fraction via: 

		Z_x,sun = (mu_x)(X_sun)10^((X/H) - 12) 

	where mu_x is the mean molecular weight of the element in amu, X_sun is 
	the solar hydrogen abundance by mass, and (X/H) = log10(Nx/NH) + 12, 
	which is what Asplund et al. (2009) reports. These calculations adopt 
	X_sun = 0.73 as the solar hydrogen abundances, also from Asplund et al. 
	(2009). 

	sources 
	-------  
	Stores strings denoting what astronomers generally believe to be the 
	dominant enrichment channels for each element. These are included purely 
	for convenience, and are adopted from Johnson (2019). This dataframe does 
	not support user customization.

		Enrichment Channels 
		------------------- 
		"CCSNE" :: core collapse supernovae 
		"SNEIA" :: type Ia supernovae 
		"AGB" :: asymptotic giant branch stars 
		"NSNS" :: binary neutron star mergers / r-process 

	References 
	========== 
	Asplund et al. (2009), ARA&A, 47, 481 
	Johnson (2019), Science, 6426, 474 
	"""

	cdef object _frame 

	def __init__(self, frame): 
		""" 
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		if isinstance(frame, dict): 
			if all(map(lambda x: isinstance(x, strcomp), frame.keys())): 
				keys = tuple([i.lower() for i in frame.keys()]) 
				fields = tuple([frame[i] for i in frame.keys()]) 
				self._frame = dict(zip(keys, fields)) 
			else: 
				raise TypeError("All keys must be of type str.") 
		else: 
			raise TypeError("""Can only initialize dataframe from type dict. \
Got: %s""" % (type(frame))) 

	def __call__(self, key): 
		""" 
		Return the same thing as __getitem__ ---> this allows users to call 
		the dataframe and achieve the same effect. 
		""" 
		return self.__getitem__(key) 

	def __getitem__(self, key): 
		""" 
		If type str, index the dataframe on key.lower(). This allows 
		case-insensitivity. If an integer, will attempt to pull the proper 
		row from a dataframe containing array-like attributes. 

		In this case, the returned value will also be a dataframe. 
		""" 
		if isinstance(key, strcomp): # If they're indexing by column label 
			if key.lower() in self.keys(): # If it's in the frame 
				return self._frame[key.lower()] 
			else: 
				# Otherwise KeyError
				raise KeyError("Unrecognized dataframe key: %s" % (key)) 

		elif isinstance(key, numbers.Number): # If they're indexing by number 
			if key % 1 == 0: # If it's an integer 
				try: 
					lengths = [len(self._frame[i]) for i in self.keys()] 
				except TypeError: 
					# This only works if every field is array-like 
					raise IndexError("""This dataframe cannot be indexed by \
a key of type int (not all fields are array-like).""") 

				# If it's within the range allowed by the minimum length 
				if abs(key) <= min(lengths) and key != min(lengths): 
					return base(dict(zip(self.keys(), 
						[self._frame[i][int(key)] for i in self.keys()]
					)))
				else:
					# Otherwise it's an IndexError 
					raise IndexError("Index out of bounds: %d" % (int(key)))

			else: 
				# If it couldn't be interpreted as an integer 
				raise IndexError("""Index must be interpreted as an integer. \
Got: %s""" % (type(key))) 

		else: 
			# If it was neither an integer nor a string 
			raise IndexError("""Only integers and strings are valid indeces. \
Got: %s""" % (type(key))) 

	def __setitem__(self, key, value): 
		""" 
		__setitem__ only allowed given a string. 
		""" 
		if isinstance(key, strcomp): 
			self._frame[key.lower()] = value 
		else: 
			raise TypeError("""Item assignment must be done via type str. \
Got: %s""" % (type(key))) 

	def __repr__(self): 
		"""
		Fancy print of the format: 
		vice.dataframe{ 
		    field1 --------> value1 
		    field_other ---> value2
		}
		"""	
		rep = "vice.dataframe{\n" 
		keys = self.keys() 
		copy = self.todict() 
		for i in keys: 
			rep += "    %s " % (i) 
			arrow = "" 
			# terminate each arrow at the same point 
			for j in range(15 - len(i)): 
				arrow += '-' 
			rep += "%s> " % (arrow) 
			try: 
				x = _pyutils.copy_array_like_object(copy[i]) 
			except TypeError: 
				x = copy[i] 
				rep += "%s\n" % (str(x)) 
				continue 
			# only array-like objects make it here 
			if len(x) >= 10: 
				rep += "[%g, %g, %g, ... , %g, %g, %g]\n" % (
					x[0], x[1], x[2], x[-3], x[-2], x[-1]) 
			else: 
				rep += "%s\n" % (str(x)) 
		rep += '}'
		return rep 

	def __str__(self): 
		""" 
		Returns self.__repr__() 
		""" 
		return self.__repr__() 
			
	def __eq__(self, other): 
		""" 
		Returns True if the dataframes have the same contents. In the case of 
		dataframes instantiated off of VICE outputs (i.e. history, mdf, and 
		output objects), returns True if they came from the same file. 
		""" 
		test = len(self.keys()) * [None] 
		for i in range(len(self.keys())): 
			try: 
				test[i] = other[self.keys()[i]] 
			except KeyError: 
				return False 
		if all(list(map(lambda x: test[x] == self._frame[self.keys()[x]], 
			range(len(self.keys()))))): 
			return True 
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

	def keys(self): 
		"""
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		return [i.lower() for i in self._frame.keys()] 

	def todict(self): 
		"""
		Signature: vice.dataframe.todict() 

		Returns the dataframe as a standard python dictionary. Note however 
		that python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		""" 
		return self._frame 


#---------------------------- ELEMENTAL SETTINGS ----------------------------# 
cdef class elemental_settings(base): 

	""" 
	A subclass of the VICE dataframe which only allows keys that are the 
	symbols of elements built into VICE [case-insensitive]. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	cdef object _name 

	def __init__(self, frame, name): 
		"""
		Parameters 
		==========
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		#=====================================================================# 
		"""
		(The above docstring is entered purely to keep the __init__ docstring 
		consistent across subclasses and instances of the VICE dataframe. 
		Below is the actual docstring for this function.) 

		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		name :: str 
			A string denoting the name of the objects stored as fields in 
			this dataframe (i.e. infall metallicity.) 
		""" 
		# super will make sure frame is a dict whose keys are of type str 
		super().__init__(frame) 
		self._name = name 

		# Now make sure each keys is a recognized element 
		for i in self.keys(): 
			if i.lower() not in _RECOGNIZED_ELEMENTS_: 
				raise ValueError("Unrecognized element: %s" % (i)) 
			else: 
				continue 
			
	def __getitem__(self, key): 
		if isinstance(key, strcomp): 
			if key.lower() in self.keys(): 
				return self._frame[key.lower()] 
			else: 
				raise IndexError("Unrecognized element: %s" % (key)) 
		else: 
			raise IndexError("Dataframe key must be of type str. Got: %s" % (
				type(key))) 


cdef class evolutionary_settings(elemental_settings): 

	""" 
	A subclass of the elemental_settings subclass which allows only numerical 
	values and functions of time to be assigned to individual elements. 

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
		super will make sure that frame is a dict with keys of type str that 
		are recognized elements 
		""" 
		super().__init__(frame, name) 

		""" 
		Now make sure that they're all either numerical values or functions of 
		time. 
		""" 
		for i in self.keys(): 
			if isinstance(self._frame[i.lower()], numbers.Number): 
				pass 
			elif callable(self._frame[i.lower()]): 
				_pyutils.args(self._frame[i.lower()], """Functional %s \
setting must take only one numerical parameter.""" % (self._name)) 
			else: 
				raise TypeError("""%s setting must be either a numerical \
value or a callable function accepting one numerical parameter. Got: %s""" % (
					self._name, type(self._frame[i.lower()]))) 

	def __setitem__(self, key, value): 
		if isinstance(key, strcomp): 
			if key.lower() in _RECOGNIZED_ELEMENTS_: 
				if isinstance(value, numbers.Number): 
					self._frame[key.lower()] = value 
				elif callable(value): 
					_pyutils.args(value, """Functional %s setting must \
accept only one numerical parameter.""" % (self._name)) 
					self._frame[key.lower()] = value 
				else: 
					raise TypeError("""%s setting must be either a numerical \
value or a function accepting one numerical parameter. Got: %s""" % (
						self._name, type(key)))   
			else: 
				raise ValueError("Unrecognized element: %s" % (key)) 
		else: 
			raise TypeError("Dataframe key must be of type str. Got: %s" % (
				type(key))) 


#-------------------- NONCUSTOMIZABLE DATAFRAME SUBCLASS --------------------#
cdef class noncustomizable(elemental_settings): 

	""" 
	A subclass of the elemental_settings subclass which throws a TypeError 
	whenever __setitem__ is called. 

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
		Instances of this class store built-in data. They must be either 
		numerical values or of type list. 
		""" 
		for i in self.keys(): 
			if not (isinstance(self._frame[i.lower()], numbers.Number) or 
				isinstance(self._frame[i.lower()], list)): 
				raise TypeError("""%s settings must be a numerical value or a \
list. Got: %s""" % (type(self._frame[i.lower()]))) 
			else: 
				continue 

	def __setitem__(self, key, value): 
		"""
		Override the base __setitem__ function to throw a TypeError whenever 
		this function is called. 
		""" 
		raise TypeError("This dataframe does not support item assignment.") 


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

	cdef object __defaults 
	cdef object _allow_funcs 
	cdef object _config_field 

	def __init__(self, frame, name, allow_funcs, config_field): 
		"""
		Parameters 
		========== 
		frame :: dict 
			A python dictionary to construct the dataframe from 
		""" 
		#=====================================================================#
		"""
		(The above docstring is entered purely to keep the __init__ docstring 
		consistent across subclasses and instances of the VICE dataframe. 
		Below is the actual docstring for this function.)

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
				_DIRECTORY_, config_field), "rb")), name) 
		else: 
			# load what was passed 
			super().__init__(frame, name) 

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

cdef class saved_yields(elemental_settings): 

	""" 
	A subclass of the VICE dataframe which holds the user's settings from 
	core collapse and type Ia supernovae at the time a singlezone simulation 
	was ran. 

	By nature, this class throws a TypeError every time __setitem__ is called. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	def __init__(self, frame, name): 
		super().__init__(frame, name) 

		""" 
		Saved yields will have already passed the necessary type-checking 
		filters, so just make sure everything in the output looks okay. No 
		need for _pyutils.args. 
		""" 
		for i in self.keys(): 
			if i.lower() not in _RECOGNIZED_ELEMENTS_: 
				raise ValueError("Unrecognized element: %s" % (i))  
			elif not (isinstance(self._frame[i.lower()], numbers.Number) or 
				callable(self._frame[i.lower()])): 
				raise TypeError("""%s yield setting must be either a \
numerical value or a callable function. Got: %s""" % (self._name, 
					type(self._frame[i.lower()]))) 
			else: 
				continue 

	def __setitem__(self, key, value): 
		""" 
		Doesn't allow customization of saved parameters by nature. 
		""" 
		raise TypeError("This dataframe does not support item assignment.") 


#----------------------------- FROMFILE SUBCLASS -----------------------------# 
cdef class fromfile(base): 

	""" 
	A subclass of the VICE dataframe which holds data from a square data file 
	containing numerical values. 

	See docstring of VICE dataframe base class for more information. 
	""" 

	cdef double **_data 
	cdef long _n_rows 
	cdef long _n_cols 
	cdef object _filename 
	cdef object _labels 

	def __init__(self, filename, labels = None): 

		super().__init__({}) 

		if os.path.exists(filename): 
			self._data = _io.read_square_ascii_file(filename.encode("latin-1")) 
			if self._data is NULL: 
				raise IOError("Failed to read data file: %s" % (filename)) 
			else: 
				self._n_rows = _io.line_count(filename.encode("latin-1")) 
				self._n_rows -= _io.header_length(filename.encode("latin-1")) 
				self._n_cols = _io.file_dimension(filename.encode("latin-1")) 
		else: 
			raise IOError("File not found: %s" % (filename)) 
		labels = _pyutils.copy_array_like_object(labels) 
		self._filename = filename 
		if all(map(lambda x: isinstance(x, strcomp), labels)): 
			if len(labels) == self._n_cols: 
				self._labels = [i.lower() for i in labels] 
			else: 
				raise ValueError("""Keyword arg 'labels' must be of length \
the file dimension. File dimension: %d. Got: %d""" % (self._n_cols, 
					len(labels))) 
		else: 
			raise TypeError("All labels must be of type str.") 

		# Free up the memory on exit 
		def cleanup(): 
			if self._data is not NULL: 
				free(self._data) 
			else:
				pass 

		atexit.register(cleanup) 

	def __getitem__(self, key): 
		"""
		Can be indexed via both str and int, allow negative indexing as well 
		""" 
		if isinstance(key, strcomp): 
			if key.lower() in self._labels: 
				arr = self._n_rows * [0.] 
				for i in range(self._n_rows): 
					arr[i] = self._data[i][self._labels.index(key.lower())] 
				return arr 
			else: 
				raise IndexError("Unrecognized dataframe key: %s" % (key)) 
		elif isinstance(key, numbers.Number) and key % 1 == 0: 
			if 0 <= key < self._n_rows: 
				return base(dict(zip(self._labels, 
					[self._data[int(key)][i] for i in range(self._n_cols)]))) 
			elif -self._n_rows <= key < 0: 
				return base(dict(zip(self._labels, 
					[self._data[self._n_rows + int(key)][i] for i in range( 
						self._n_cols)]))) 
			else: 
				raise IndexError("Index out of bounds: %d" % (key)) 
		else: 
			raise IndexError("""Dataframe key must be of type str or int. \
Got: %s""" % (type(key))) 

	def __setitem__(self, key, value): 
		""" 
		Allow item assignment via type str only. Must be of the same length as 
		the data itself. 
		""" 
		value = _pyutils.numeric_check(value, TypeError, 
			"All elements of assigned array must be real numbers.") 
		if isinstance(key, strcomp): 
			if len(value) == self._n_rows: 
				if key.lower() in self._labels: 
					for i in range(self._n_rows): 
						self._data[i][self._labels.index(
							key.lower())] = value[i] 
				else: 
					for i in range(self._n_rows): 
						self._data[i] = <double *> realloc(self._data[i], 
							(self._n_cols + 1) * sizeof(double)) 
						self._data[i][self._n_cols] = value[i] 
					self._n_cols += 1 
			else: 
				raise ValueError("""Array length mismatch. Got: %d. Must be: \
%d""" % (len(value), self._n_rows)) 
		elif isinstance(key, numbers.Number) and key % 1 == 0: 
			# raise a custom error for users attempting to assign rows. 
			raise TypeError("This dataframe does not support row assignment.") 
		else: 
			raise TypeError("""Item assignment only allowed for type str. \
Got: %s""" % (type(key))) 

	def __eq__(self, other): 
		""" 
		Returns True if other is also a fromfile object and points to the same 
		file as self. 
		""" 
		if isinstance(other, fromfile): 
			return self._filename == other._filename 
		else: 
			return False 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions inside with statements and automatically frees 
		memory. 
		""" 
		if self._data is not NULL: 
			free(self._data) 
		else: 
			pass 
		return exc_value is not None 

	@property 
	def size(self): 
		""" 
		The (length, width) of the dataframe. 
		""" 
		return tuple([self._n_rows, self._n_cols]) 
		
	def keys(self): 
		"""
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		return self._labels 

	def todict(self): 
		"""
		Signature: vice.dataframe.todict() 

		Returns the dataframe as a standard python dictionary. Note however 
		that python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		""" 
		return dict(zip(self._labels, 
			[self.__getitem__(i) for i in self._labels])) 


#----------------------------- HISTORY SUBCLASS -----------------------------# 
cdef class history(fromfile): 

	""" 
	A subclass of the VICE dataframe which holds data from a square data file 
	containing numerical values. This particular subclass allows the user to 
	call __getitem__ with '[m/h]' and 'z' to calculate the total (scaled) 
	metallicity of the interstellar medium at each output time automatically. 

	See docstring of VICE dataframe base class for more information. 

	See section 5.4 of VICE's science documentation (available at 
	https://github.com/giganano/VICE/blob/master/docs/) for information on 
	the scaled metallicity of the interstellar medium. 
	""" 

	cdef double _adopted_solar_z 

	def __init__(self, filename, adopted_solar_z, labels = None): 
		super().__init__(filename, labels = labels) 
		if isinstance(adopted_solar_z, numbers.Number): 
			self._adopted_solar_z = adopted_solar_z 
		else: 
			raise TypeError("""Adopted solar metallicity must be numerical \
value. Got: %s""" % (type(adopted_solar_z))) 

	def __getitem__(self, key): 
		"""
		Can be indexed via both str and int, allow negative indexing as well. 
		Special strings [m/h] and z recognized for automatic calculation of 
		scaled total ISM metallicity. 
		""" 
		if isinstance(key, strcomp): 
			if key.lower() in ["[m/h]", "z"]: 
				from ._builtin_dataframes import solar_z 

				# Add up the total metals present 
				arr = self._n_rows * [0.] 
				# The column numbers to add up and the elements tracked 
				cols = list(filter(lambda x: x.startswith("z("), 
					self._labels)) 
				elements = [i[2:-1] for i in cols] 
				solar = sum([solar_z[i] for i in elements]) 

				for i in range(len(arr)): 
					for j in cols: 
						arr[i] += self._data[i][j] 
					arr[i] /= solar 

				del solar_z 
				if key.lower() == "z": 
					return [self._adopted_solar_z * i for i in arr] 
				elif key.lower() == "[m/h]": 
					return [m.log10(i) if i != 0 else -float(
						"inf") for i in arr] 
				else: 
					raise SystemError("Internal Error") 
			elif '/' in key: 
				"""
				Attempt to flip the key. __XoverY raises a ValueError if this 
				isn't possible, so this can be done with a simple try-except 
				block. 
				"""
				try: 
					return self.__XoverY(key) 
				except ValueError: 
					return super().__getitem__(key) 
			else: 
				return super().__getitem__(key) 
		else: 
			return super().__getitem__(key) 


	def __XoverY(self, key): 
		""" 
		If the user asks for the abundance ratio [X/Y] when the simulation 
		tracked [Y/X], this function automatically calulates the requested 
		abundance ratio. This is not done for the MDF outputs because that 
		involves flipping the bins, not the values of the MDF themselves. 
		""" 
		element1 = key.split('/')[0][1:] 
		element2 = key.split('/')[1][:-1] 
		if "[%s/h]" % (element1.lower()) not in self.keys(): 
			raise ValueError 
		elif "[%s/h]" % (element2.lower()) not in self.keys(): 
			raise ValueError 
		else: 
			return list(map(lambda x, y: x - y, 
				self.__getitem__("[%s/h]" % (element1.lower())), 
				self.__getitem__("[%s/h]" % (element2.lower()))
			))



