# cython: language_level = 3, boundscheck = False 
""" 
This file implements the history object, a subclass of the fromfile object. 
This class is designed to read in and make calculations with the history.out 
file associated with outputs of the singlezone class. 
""" 

from ..._globals import _VERSION_ERROR_ 
from ..outputs import _output_utils 
from .. import _pyutils 
from . import _base 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from libc.stdlib cimport malloc, free 
from .._cutils cimport set_string 
from . cimport _history 


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

	# cdef char **_elements 
	# cdef unsigned int n_elements 
	# cdef double *solar 
	# cdef double Z_solar 

	def __init__(self, filename = None, adopted_solar_z = None, 
		labels = None): 
		super().__init__(filename = filename, labels = 
			_output_utils._load_column_labels_from_file_header(filename)) 
		elements = self._load_elements() 
		self._n_elements = <unsigned> len(elements) 
		self._elements = <char **> malloc (self._n_elements * sizeof(char *)) 
		for i in range(self._n_elements): 
			self._elements[i] = <char *> malloc ((len(elements) + 1) * 
				sizeof(char)) 
			set_string(self._elements[i], elements[i]) 
		self._solar = <double *> malloc (self._n_elements * sizeof(double)) 
		from ._builtin_dataframes import solar_z 
		for i in range(self._n_elements): 
			self._solar[i] = solar_z[elements[i]] 
		self._Z_solar = adopted_solar_z 

	def _load_elements(self): 
		elements = [] 
		for i in _output_utils._load_column_labels_from_file_header(self.name):  
			if i.startswith("mass("): 
				# Find elements based on the columns of reported masses
				elements.append("%s" % (i.split('(')[1][:-1].lower())) 
			else: 
				continue 
		return tuple(elements[:]) 

	def __getitem__(self, key): 
		"""
		Can be indexed via both str and int, allow negative indexing as well. 
		Special strings [m/h] and z recognized for automatic calculation of 
		scaled total ISM metallicity. 
		""" 
		if isinstance(key, strcomp): 
			return self.__subget__str(key) 
		elif isinstance(key, numbers.Number) and key % 1 == 0: 
			return self.__subget__int(key) 
		else: 
			# No error yet, other possibilities in super's __getitem__ 
			return super().__getitem__(key) 

	def __subget__str(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str 
		""" 
		# See docstrings of subroutines for further info 
		if key.lower().startswith("z(") and key.endswith(')'): 
			return self.__subget__str_z(key) 
		elif key.lower() == "y": 
			return self.__subget__str_y(key) 
		elif key.lower() == "z": 
			return self.__subget__str_ztot(key) 
		elif key.lower() == "[m/h]": 
			return self.__subget__str_logztot(key) 
		elif key.startswith('[') and key.endswith(']') and '/' in key: 
			return self.__subget__str_logzratio(key) 
		else: 
			# No error yet, other possibilities in super's __getitem__ 
			return super().__subget__str(key) 

	def __subget__str_z(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting a metallicity by mass Z of a given element. 
		""" 
		cdef double *item 
		cdef char *copy 
		element = key.split('(')[1][:-1].lower() 
		copy = <char *> malloc ((len(element) + 1) * sizeof(char)) 
		set_string(copy, element.lower()) 
		item = _history.Z_element(self._ff, copy) 
		free(copy) 
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise KeyError("Element not tracked by simulation: %s" % (
				element)) 

	def __subget__str_y(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting the helium mass fraction Y. 
		""" 
		return self.__subget__str_z("z(he)") 

	def __subget__str_ztot(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting the total metallicity by mass Z
		""" 
		cdef double *item 
		item = _history.Zscaled(self._ff, self._n_elements, 
			self._elements, self._solar, self._Z_solar)  
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise SystemError("Internal Error") 

	def __subget__str_logztot(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting the log of the total metallicity by mass [M/H]. 
		""" 
		cdef double *item
		item = _history.logarithmic_scaled(self._ff, self._n_elements, 
			self._elements, self._solar)  
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise SystemError("Internal Error") 

	def __subget__str_logzratio(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting a logarithmic abundance ratio [X/Y]. This is generalized to 
		handle absolute abundances in the case that [X/H] is passed. 
		""" 
		cdef double *item 
		cdef char *copy 
		cdef char *copy2 
		element1 = key.split('/')[0][1:] 
		element2 = key.split('/')[1][:-1] 
		copy = <char *> malloc ((len(element1) + 1) * sizeof(char)) 
		copy2 = <char *> malloc ((len(element2) + 1) * sizeof(char)) 
		set_string(copy, element1.lower()) 
		set_string(copy2, element2.lower()) 
		item = _history.logarithmic_abundance_ratio(self._ff, 
			copy, copy2, self._elements, self._n_elements, self._solar) 
		free(copy) 
		free(copy2) 
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise KeyError("Unrecognized dataframe key: %s" % (key)) 

	def __subget__int(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type int. 
		""" 
		cdef double *item 
		if 0 <= key < self._ff[0].n_rows: 
			item = _history.history_row(self._ff, <unsigned long> key, 
				self._elements, self._n_elements, self._solar, 
				self._Z_solar) 
		elif abs(key) <= self._ff[0].n_rows: 
			item = _history.history_row(self._ff, 
				self._ff[0].n_rows - <unsigned long> abs(key), 
				self._elements, self._n_elements, self._solar, 
				self._Z_solar) 
		else: 
			raise IndexError("Index out of bounds: %d" % (int(key))) 
		if item is not NULL: 
			x = [item[i] for i in range(_history.row_length(self._ff, 
				self._n_elements))]   
			free(item) 
			return _base.base(dict(zip(self.keys(), x))) 
		else: 
			raise SystemError("Internal Error") 

	def keys(self): 
		"""
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		keys = super().keys() 
		elements = self._load_elements() 
		for i in elements: 
			keys.append("z(%s)" % (i)) 
		for i in elements: 
			keys.append("[%s/h]" % (i)) 
		for i in range(1, len(elements)): 
			for j in range(i): 
				keys.append("[%s/%s]" % (elements[i], elements[j])) 
		keys.append("z") 
		keys.append("[m/h]") 
		return keys 

