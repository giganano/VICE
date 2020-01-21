# cython: language_level = 3, boundscheck = False 
""" 
This file implements the fromfile object, a subclass of the VICE dataframe 
base class. This objects stores data pulled from a square ascii text file 
whose header is delimited with '#'. All files that VICE produces and has 
built-in are of this format. 
""" 

from ..._globals import _VERSION_ERROR_ 
from .. import _pyutils 
from . import _base
import numbers 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from libc.stdlib cimport malloc, free 
from libc.string cimport strlen, strcmp 
from .._cutils cimport set_string, copy_pylist
from . cimport _fromfile 
# from . cimport _objects 
# from ._base cimport base 


#----------------------------- FROMFILE SUBCLASS -----------------------------# 
cdef class fromfile(base): 

	""" 
	A subclass of the VICE dataframe which holds data from a square data file 
	containing numerical values. 

	See docstring of VICE dataframe base class for more information. 
	""" 
	# cdef FROMFILE *_ff 

	# Extra keyword args to __cinit__ and __init__ to not break history object 
	def __cinit__(self, filename = None, adopted_solar_z = None, 
		labels = None): 
		self._ff = _fromfile.fromfile_initialize() 

	def __init__(self, filename = None, adoped_solar_z = None, 
		labels = None): 
		super().__init__({}) 
		if os.path.exists(filename): 
			# Set the filename and read in the data 
			set_string(self._ff[0].name, filename) 
			_fromfile.fromfile_read(self._ff) 
			if self._ff[0].data is NULL: # Error reading the file 
				raise IOError("Error reading square data file: %s" % (filename)) 
			labels = _pyutils.copy_array_like_object(labels) 
			labels = list(dict.fromkeys(labels)) 
			if len(labels) == self._ff[0].n_cols: 
				if all(map(_pyutils.is_ascii, labels)): 
					# Copy labels into C 
					self._ff[0].labels = <char **> malloc (
						self._ff[0].n_cols * sizeof(char *)) 
					for i in range(self._ff[0].n_cols): 
						self._ff[0].labels[i] = <char *> malloc (
							(len(labels[i]) + 1) * sizeof(char)) 
						set_string(self._ff[0].labels[i], 
							labels[i]) 
				else: 
					raise ValueError("All labels must be ascii.")
			else: 
				raise ValueError("""Keyword arg 'labels' must be of \
length the file dimension. File dimension: %d. Got: %d""" % (
					self._ff[0].n_cols, len(labels))) 
		else: 
			raise IOError("File not found: %s" % (filename)) 

	def __dealloc__(self): 
		_fromfile.fromfile_free(self._ff) 

	def __getitem__(self, key): 
		""" 
		Can be indexed via both str and int, allow negative indexing as well 
		""" 
		if isinstance(key, strcomp): 
			return self.__subget__str(key) 
		elif isinstance(key, numbers.Number): 
			return self.__subget__number(key) 
		else: 
			raise KeyError("""Dataframe key must be of type str or int. \
Got: %s""" % (type(key))) 

	def __subget__str(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str 
		""" 
		cdef double *item 
		cdef char *copy 
		if _pyutils.is_ascii(key): 
			copy = <char *> malloc ((len(key) + 1) * sizeof(char)) 
			set_string(copy, key.lower()) 
			item = _fromfile.fromfile_column(self._ff, copy) 
			free(copy) 
			if item is not NULL: 
				x = [item[i] for i in range(self._ff[0].n_rows)] 
				free(item) 
				return x 
			else: 
				raise KeyError("Unrecognized key: %s" % (key)) 
		else: 
			raise KeyError("All keys and labels must be ascii.") 

	def __subget__number(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type int 
		""" 
		cdef double *item 
		if key % 1 == 0: 
			# Get the row from the data, allowing negative indexing 
			if 0 <= key < self._ff[0].n_rows: 
				item = _fromfile.fromfile_row(self._ff, int(key)) 
			elif key < 0 and -key <= self._ff[0].n_rows: 
				item = _fromfile.fromfile_row(self._ff, 
					self._ff[0].n_rows + int(key)) 
			else: 
				raise IndexError("Index out of bounds: %d" % (int(key))) 
		else: 
			raise KeyError("""Dataframe key must be of type str or int. \
Got: %s""" % (type(key))) 
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_cols)] 
			free(item) 
			return _base.base(dict(zip(self.keys(), x))) 
		else: 
			raise SystemError("Internal Error") 

	def __setitem__(self, key, value): 
		""" 
		Allow item assignment via type str only. Must be of the same length as 
		the data itself. 
		""" 
		cdef char *copy 
		value = _pyutils.copy_array_like_object(value) 
		_pyutils.numeric_check(value, TypeError, 
			"All elements of assigned array must be real numbers.") 
		if isinstance(key, strcomp): 
			if <unsigned> len(value) == self._ff[0].n_rows: 
				copy = <char *> malloc ((len(key) + 1) * sizeof(char)) 
				set_string(copy, key.lower()) 
				if _fromfile.fromfile_modify_column(self._ff, key, 
					copy_pylist(value)): 
					raise SystemError("Internal Error") 
				else: 
					free(copy) 
			else: 
				raise ValueError("""Array length mismatch. Got: %d. Must be: \
%d""" % (len(value), self._ff[0].n_rows)) 
		elif isinstance(key, numbers.Number) and key % 1 == 0: 
			raise TypeError("""This dataframe does not support row assignment. \
Item assignment only allows for type str. Got: %s""" % (type(key)))  
		else: 
			raise TypeError("""Item assignment only allowed for type str. \
Got: %s""" % (type(key))) 

	def __eq__(self, other): 
		""" 
		Returns True if other is also a fromfile object and points to the same 
		file as self. 
		""" 
		if isinstance(other, fromfile): 
			return not strcmp(self._ff[0].name, other._ff[0].name) 
		else: 
			return False 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		""" 
		Raises all exceptions inside with statements and automatically frees 
		memory. 
		""" 
		return exc_value is not None 

	@property 
	def name(self): 
		""" 
		The name of the file that this data was imported from 
		""" 
		return "".join([chr(self._ff[0].name[i]) for i in range(
			strlen(self._ff[0].name))]) 

	@property 
	def size(self): 
		""" 
		The (length, width) of the dataframe. 
		""" 
		return tuple([self._ff[0].n_rows, self._ff[0].n_cols]) 
		
	def keys(self): 
		"""
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		labels = self._ff[0].n_cols * [None] 
		for i in range(self._ff[0].n_cols): 
			labels[i] = "".join([chr(self._ff[0].labels[i][j]) for j in range(
				strlen(self._ff[0].labels[i]))]) 
		return labels 

	def todict(self): 
		"""
		Signature: vice.dataframe.todict() 

		Returns the dataframe as a standard python dictionary. Note however 
		that python dictionaries are case-sensitive, and are thus less 
		versatile than this object. 
		""" 
		return dict(zip(self.keys(), 
			[self.__getitem__(i) for i in self.keys()])) 

