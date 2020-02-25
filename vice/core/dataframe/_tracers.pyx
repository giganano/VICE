# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..._globals import _VERSION_ERROR_ 
from ..outputs import _output_utils 
from .. import _pyutils 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 
from libc.stdlib cimport malloc, free 
from libc.string cimport strlen 
from .._cutils cimport set_string 
from . cimport _tracers 
from . cimport _fromfile 
from . cimport _base 


cdef class tracers(history): 

	""" 
	A subclass of the VICE dataframe which holds data from a square data file 
	containing numerical values. This particular subclass allows users to call 
	__getitem__ with '[m/h]', 'z', and 'age' to calculate the total (scaled) 
	metallicity of stars in multizone simulations automatically. 

	See docstring of VICE dataframe base class for more information. 

	See Also 
	======== 
	VICE dataframe base class 

	Section 5.4 of VICE's science documentation (available at 
	https://github.com/giganano/VICE/blob/master/docs/) for information on 
	the scaled metallicity of the interstellar medium and stars. 
	""" 

	def __init__(self, filename = None, adopted_solar_z = None, 
		labels = None): 
		super().__init__(filename = filename, 
			adopted_solar_z = adopted_solar_z, 
			labels = labels) 

	def _load_elements(self): 
		""" 
		Override this function of the history class, which looks for columns 
		of reported masses to find the tracked elements. Tracer output files 
		do not have such information, but do have metallicities instead. 
		""" 
		elements = [] 
		for i in _output_utils._load_column_labels_from_file_header(self.name): 
			if i.startswith("z("): 
				# Find elements based on the columns of reported metallicities 
				elements.append(i.split('(')[1][:-1].lower()) 
			else: continue 
		return tuple(elements[:]) 

	def __subget__str(self, key): 
		# see docstring of subroutines for further info 
		if key.lower().startswith("z(") and key.endswith(')'): 
			return self.__subget__str_z(key) 
		elif key.lower() == "y": 
			return self.__subget__str_y(key) 
		elif key.lower() == "z": 
			return self.__subget__str_ztot(key) 
		elif key.lower() == "[m/h]": 
			return self.__subget__str_logztot(key) 
		elif key.lower() == "age": 
			return self.__subget__str_age(key) 
		elif key.startswith('[') and key.endswith(']') and '/' in key: 
			return self.__subget__str_logzratio(key) 
		else: 
			# No error yet, other possibilities in super's __getitem__ 
			return super().__subget__str(key) 

	def __subget__str_z(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting a metallicity by mass Z of a given element. 

		Unlike the history object, Z(x) for all elements x is stored in the 
		output file. 
		""" 
		cdef double *item 
		cdef char *copy 
		element = key.split('(')[1][:-1].lower() 
		copy = <char *> malloc ((len(element) + 1) * sizeof(char)) 
		set_string(copy, element.lower()) 
		# item = _fromfile.fromfile_column(self._ff, copy) 
		item = _tracers.tracers_Z_element(self._ff, copy) 
		free(copy) 
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise KeyError("Element not tracked by simulation: %s" % (
				element)) 

	def __subget__str_ztot(self, key): 
		""" 
		Performs the __getitem__ operation when the key is of type str and is 
		requesting the total metallicity by mass Z 
		""" 
		cdef double *item 
		item = _tracers.tracers_Zscaled(self._ff, self._n_elements, 
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
		item = _tracers.tracers_logarithmic_scaled(self._ff, self._n_elements, 
			self._elements, self._solar) 
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise SystemError("Internal Error") 

	def __subget__str_age(self, key): 
		cdef double *item 
		item = _tracers.tracers_age(self._ff) 
		if item is not NULL: 
			x = [item[i] for i in range(self._ff[0].n_rows)] 
			free(item) 
			return x 
		else: 
			raise SystemError("Internal Error") 

	def __subget__str_logzratio(self, key): 
		cdef double *item 
		cdef char *copy 
		cdef char *copy2 
		element1 = key.split('/')[0][1:] 
		element2 = key.split('/')[1][:-1] 
		copy = <char *> malloc ((len(element1) + 1) * sizeof(char)) 
		copy2 = <char *> malloc ((len(element2) + 1) * sizeof(char)) 
		set_string(copy, element1.lower()) 
		set_string(copy2, element2.lower()) 
		item = _tracers.tracers_logarithmic_abundance_ratio(self._ff, copy, 
			copy2, self._elements, self._n_elements, self._solar) 
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
			item = _tracers.tracers_row(self._ff, <unsigned long> key, 
				self._elements, self._n_elements, self._solar, self._Z_solar)  
		elif abs(key) <= self._ff[0].n_rows: 
			item = _tracers.tracers_row(self._ff, 
				self._ff[0].n_rows - <unsigned long> abs(key), 
				self._elements, self._n_elements, self._solar, self._Z_solar) 
		else: 
			raise IndexError("Index out of bounds: %d" % (int(key))) 
		if item is not NULL: 
			x = [item[i] for i in range(_tracers.tracers_row_length(self._ff, 
				self._n_elements))] 
			free(item) 
			return _base.base(dict(zip(self.keys(), x))) 

	def keys(self): 
		""" 
		Signature: vice.dataframe.keys() 

		Returns the dataframe keys in their lower-case format 
		""" 
		labels = self._ff[0].n_cols * [None] 
		for i in range(self._ff[0].n_cols): 
			labels[i] = "".join([chr(self._ff[0].labels[i][j]) for j in range(
				strlen(self._ff[0].labels[i]))]) 
		elements = self._load_elements() 
		for i in elements: 
			labels.append("[%s/h]" % (i)) 
		for i in range(1, len(elements)): 
			for j in range(i): 
				labels.append("[%s/%s]" % (elements[i], elements[j])) 
		labels.append("z") 
		labels.append("age") 
		return labels 

