# cython: language_level = 3, boundscheck = False 

from libc.stdlib cimport malloc, free 
from .._globals import _VERSION_ERROR_ 
from .._globals import _RECOGNIZED_IMFS_ 
from .._globals import ScienceWarning 
from . import _pyutils 
from ..yields import agb 
from ..yields import ccsne 
from ..yields import sneia 
import warnings 
import numbers 
import math as m 
import sys 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

from libc.stdlib cimport malloc, free 
from .objects._imf cimport IMF_ 
from .objects._agb cimport AGB_YIELD_GRID 
from .objects._callback_1arg cimport CALLBACK_1ARG 
from .objects._callback_2arg cimport CALLBACK_2ARG 


cdef extern from "../src/utils.h": 
	double *binspace(double start, double stop, long N) 
	void set_char_p_value(char *dest, int *ords, int length) 

cdef extern from "../src/imf.h": 
	double IMF_STEPSIZE 
	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 

cdef extern from "../src/objects.h": 
	CALLBACK_1ARG *callback_1arg_initialize() 
	void callback_1arg_free(CALLBACK_1ARG *cb1) 
	CALLBACK_2ARG *callback_2arg_initialize() 
	void callback_2arg_free(CALLBACK_2ARG *cb2) 


cdef inline void callback_1arg_setup(CALLBACK_1ARG *cb1, value) except *: 
	""" 
	Setup a callback object for a python function. Assign the assumed_constant 
	if value is a number. This allows parameters which may be either a constant 
	or a varying function of time to always use the same callback object. 

	Parameters 
	========== 
	cb1 :: CALLBACK_1ARG * 
		A pointer to the callback object for the function 
	value :: <function> or real number 
		The python function to get a callback object for. This must accept 
		exactly one positional argument if callable, as the name of the object 
		suggests, and is assumed to already be wrapped by one of the callback1 
		classes. If a real number, a function is still assigned to one that 
		always evaluates to that value.  

	Raises 
	====== 
	TypeError :: 
		::	value is neither a number nor callable 
		::	value is callable and does not accept exactly one positional 
			argument 
			
	See Also 
	======== 
	vice/core/callback.py 
	""" 
	if callable(value): 
		if _pyutils.arg_count(value) == 1: 
			cb1[0].callback = &callback_1arg 
			cb1[0].user_func = <void *> value 
		else: 
			raise TypeError("""Function must accept exactly one positional \
argument.""") 
	elif isinstance(value, numbers.Number): 
		cb1[0].user_func = NULL 
		cb1[0].assumed_constant = <double> value 
	else: 
		raise TypeError("""Must be either a real number or a callable object. \
Got: %s""" % (type(value))) 


cdef inline void callback_2arg_setup(CALLBACK_2ARG *cb2, value) except *: 
	""" 
	Setup a callback object for a python function. Assign the assumed_constant 
	if value is a number. This allows parameters which may be either a constant 
	or a varying function to always use the same callback object. 

	Parameters 
	========== 
	cb2 :: CALLBACK_2ARG * 
		A pointer to the callback object for the function 
	value :: <function> or real number 
		The python function to get a callback object for. This must accept 
		exactly two positional arguments if callable, as the name of the 
		object suggests, and is assumed to already be wrapped by one of the 
		callback2 classes. If a real number, a function is still assigned to 
		one that always evaluates to that value. 

	Raises 
	====== 
	TypeError :: 
		::	value is neither a number nor callable 
		::	value is callable and does not accept exactly two positional 
			arguments 

	See Also 
	======== 
	vice/core/callback.py 
	""" 
	if callable(value): 
		if _pyutils.arg_count(value) == 2: 
			cb2[0].callback = &callback_2arg 
			cb2[0].user_func = <void *> value 
		else: 
			raise TypeError("""Function must accept exactly two positional \
arguments.""") 
	elif isinstance(value, numbers.Number): 
		cb2[0].user_func = NULL 
		cb2[0].assumed_constant = <double> value 
	else: 
		raise TypeError("Function must be a callable object. Got: %s" % (
			type(value))) 


cdef inline double callback_1arg(double x, void *f): 
	""" 
	Call a function defined in Python from C. 

	Parameters 
	========== 
	x :: real number 
		The value to evaluate the function at. Called under the hood in C, this 
		will always be a real number. 
	f :: <function> 
		A void pointer to the PyObject corresponding to the user's function 
		which they've defined in python 

	Returns 
	======= 
	result :: real number 
		f(x), if the function returns a numerical value. If the value is 
		non-numerical, a value of 0 will be assumed. 

	Raises 
	====== 
	ScienceWarning :: 
		::	A non-numerical value is returned from the function, forcing it to 
			assume a default value of zero. 

	See Also 
	======== 
	vice/core/callback.py 
	""" 
	# pythonic callback objects handle these errors 
	return <double> (<object> f)(x) 


cdef inline double callback_2arg(double x, double y, void *f): 
	""" 
	Call a function defined in Python from C. 

	Parameters 
	========== 
	x :: real number 
		The first numerical argument to the function. 
	y :: real number 
		The second numerical argument to the function. 
	f :: <function> 
		A void pointer to the PyOjbect corresponding to the user's function 
		which they've defined in python. 

	Returns 
	======= 
	result :: real number 
		f(x, y), if the function returns a numerical value. If the value is 
		non-numerical, a value of 0 will be assumed. 

	Raises 
	====== 
	ScienceWarning :: 
		::	A non-numerical value is returned from the function, forcing it to 
			assume a default value of zero. 

	See Also 
	======== 
	vice/core/callback.py 
	""" 
	# pythonic callback objects now handle these errors 
	return <double> (<object> f)(x, y) 


cdef inline void setup_imf(IMF_ *imf, IMF) except *: 
	""" 
	Setup an already malloc'ed IMF_ object. 

	Parameters 
	========== 
	imf :: 	IMF_ *
		A pointer to the IMF_ object 
	IMF :: str [case-insensitive] or <function> 
		The user's IMF prescription - either a string denoting a built-in IMF 
		or a callback object associated with a custom IMF constructed by the 
		user. 

	Raises 
	====== 
	TypeError :: 
		::	IMF is neither a string nor a function 
	ValueError :: 
		::	A string is not recognized as a built-in IMF 

	See Also 
	======== 
	vice/core/callback.py 
	""" 
	if isinstance(IMF, strcomp): 
		if IMF.lower() in _RECOGNIZED_IMFS_: 
			set_string(imf[0].spec, IMF.lower()) 
		else: 
			raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	elif callable(IMF): 
		callback_1arg_setup(imf[0].custom_imf, IMF) 
		set_string(imf[0].spec, "custom") 
	else: 
		raise TypeError("""IMF must be either a string denoting a built-in \
IMF or a callable function. Got: %s""" % (type(IMF))) 


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


cdef inline double **copy_2Dpylist(pylist) except *: 
	""" 
	Allocate memory for a 2-D double pointer array and copy each element of a 
	python list into the resultant C array. 

	Parameters 
	========== 
	pylist :: array-like 
		A python 2D array-like object that can be indexed via pylist[x][y] 

	Raises 
	====== 
	TypeError :: 
		:: pylist has a non-numerical value 
	""" 
	cdef double **copy = <double **> malloc (len(pylist) * sizeof(double *)) 
	for i in range(len(pylist)): 
		copy[i] = <double *> malloc (len(pylist[i]) * sizeof(double)) 
		for j in range(len(pylist[i])): 
			if isinstance(pylist[i][j], numbers.Number): 
				copy[i][j] = pylist[i][j] 
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

