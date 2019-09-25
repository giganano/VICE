# cython: language_level = 3, boundscheck = False 

from libc.stdlib cimport malloc, free 
from .._globals import _VERSION_ERROR_ 
from .._globals import _RECOGNIZED_IMFS_ 
from . import _pyutils 
import numbers 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

from libc.stdlib cimport malloc, free 
from ._objects cimport IMF_ 
cdef extern from "../src/utils.h": 
	double *binspace(double start, double stop, long N) 
	void set_char_p_value(char *dest, int *ords, int length) 
cdef extern from "../src/imf.h": 
	double IMF_STEPSIZE 
	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 


cdef inline void setup_imf(IMF_ *imf, IMF) except *: 
	cdef double *mapped 
	if callable(IMF): 
		_pyutils.args(IMF, """Stellar IMF must accept only one numerical \
parameter.""")
		set_string(imf[0].spec, "custom") 
		masses = _pyutils.range_(imf[0].m_lower, imf[0].m_upper, IMF_STEPSIZE) 
		mapped = <double *> malloc (len(masses) * sizeof(double)) 
		for i in range(len(masses)): 
			mapped[i] = IMF(masses[i]) 
		if (imf_set_mass_distribution(imf, mapped)): 
			free(mapped) 
			raise ArithmeticError("""Custom IMF evaluated to negative, inf, \
or nan for at least one stellar mass.""") 
		else: 
			free(mapped) 
	elif isinstance(IMF, strcomp): 
		if IMF.lower() in _RECOGNIZED_IMFS_: 
			set_string(imf[0].spec, IMF.lower()) 
		else: 
			raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	else: 
		raise TypeError("""IMF must be either a string denoting a built-in \
initial mass function or a callable function. Got: %s""" % (type(IMF))) 



cdef inline void set_string(char *dest, pystr) except *: 
	""" 
	Sets a string value (char *) given the python string it should be 
	set to. 

	Parameters 
	========== 
	dest :: char * 
		The char pointer to put the copy of the python string into 
	pystr :: str 
		The python string to copy into C 

	Notes 
	===== 
	This practice is employed here due to a likely bug within the Cython 
	implementation. In practice, both passing <bytes> strings and using 
	strcpy to move python strings into C have proven unstable. The method 
	that performs the best in practice is to allocate memory for all C 
	object char* attributes upon initialization, then fill them with the 
	ordinal numbers (ascii indeces), and use C to force the null terminator 
	'\0' at the end. This is a rather brute force approach that skirts 
	other dependencies and performs better than others in practice. 
	""" 
	if not _pyutils.is_ascii(pystr): 
		raise ValueError("Must be ascii string.") 
	else: 
		pass 
	cdef int *ords = ordinals(pystr) 
	set_char_p_value(dest, ords, len(pystr)) 
	free(ords) 

cdef inline int *ordinals(pystr) except *: 
	""" 
	Get a C char * from a python string. 

	Parameters 
	========== 
	pystr :: str 
		A python string of any kind 

	Returns 
	======= 
	A C char * with the same contents as pystr. 

	Raises 
	====== 
	TypeError :: 
		:: pystr is not a pythong string 
	""" 
	if not isinstance(pystr, strcomp): 
		raise TypeError("Must be of type str. Got: %s" % (type(pystr))) 
	else: 
		pass 

	cdef int *copy = <int *> malloc (len(pystr) * sizeof(int)) 
	for i in range(len(pystr)): 
		copy[i] = ord(pystr[i]) 
	return copy 


cdef inline double *copy_pylist(pylist) except *: 
	"""
	Allocate memory for a double pointer and copy each element of a python 
	list into the resultant C array. 

	Parameters 
	========== 
	pylist :: array-like 
		A python 1D array-like object than can be indexed via pylist[x] 

	Raises 
	====== 
	TypeError :: 
		:: pylist has a non-numerical value 
	""" 
	cdef double *copy = <double *> malloc (len(pylist) * sizeof(double)) 
	for i in range(len(pylist)): 
		if isinstance(pylist[i], numbers.Number): 
			copy[i] = pylist[i] 
		else: 
			raise TypeError("Non-numerical value detected.") 
	return copy 

cdef inline double *map_pyfunc_over_array(pyfunc, pyarray) except *: 
	"""
	Map a python function across an array of values and store the output in 
	a double pointer. 

	Parameters 
	========== 
	pyfunc :: callable python function 
		The function to map. Must take only one parameter (i.e. pyfunc(x)) 
	pyarray :: array-like 
		The array to map pyfunc over. Must be 1D and taking only numerical 
		values. 

	Returns 
	======= 
	mapped :: <double *> 
		The double pointer to the C array containing the mapped values 

	Raises 
	====== 
	TypeError :: 
		:: pyarray contains a non-numerical value 
		:: pyfunc maps to a non-numerical value 
		:: pyfunc is not callable 
	""" 
	if not callable(pyfunc): 
		raise TypeError("Must be a callable function. Got: %s" % (
			type(pyfunc)))
	else: 
		pass 
	cdef double *mapped = <double *> malloc (len(pyarray) * sizeof(double)) 
	for i in range(len(pyarray)): 
		if isinstance(pyarray[i], numbers.Number): 
			if isinstance(pyfunc(pyarray[i]), numbers.Number): 
				mapped[i] = pyfunc(pyarray[i]) 
			else: 
				raise TypeError("Function mapped to non-numerical value.") 
		else: 
			raise TypeError("Non-numerical value detected.") 
	return mapped  

