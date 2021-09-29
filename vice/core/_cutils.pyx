# cython: language_level = 3, boundscheck = False 
r""" 
C Utilities 
===========

.. warning:: User access of this module is discouraged. 

Contains under-the-hood utility functions for VICE's C side. 
""" 

from __future__ import absolute_import 
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
from libc.string cimport strlen 
from . cimport _cutils 


cdef class progressbar: 

	r""" 
	**VICE Developer's Documentation** 

	A simple progressbar object wrapping the one implements in C at 
	./vice/src/io/progressbar.c. 

	**Signature**: progressbar(maxval = 10) 

	Parameters 
	----------
	maxval : ``int`` [positive definite] 
		The maximum number of iterations in the progressbar. 

	Attributes 
	----------
	maxval : ``int`` [positive definite] 
		The maximum number of iterations in the progressbar. 
	left_hand_side : ``str`` 
		The string to print to the left of the progressbar. Defaults to the 
		current and maximum number of iterations. 
	right_hand_side : ``str`` 
		The string to print to the right of the progressbar. Defaults to an 
		estimate of the time remaining in the calculation. 

	Functions 
	---------
	finish : instance method 
		Set the current number of iterations equal to self.maxval and move to a 
		new line in the terminal. 
	update : instance method 
		Update the number of iterations in the progressbar and refresh what's 
		printed on the terminal screen. 
	""" 

	def __cinit__(self, maxval = 10): 
		self._pb = _cutils.progressbar_initialize(<unsigned long> 10) 
		self.maxval = maxval 

	def __init__(self, maxval = 10): 
		pass 

	def __dealloc__(self): 
		_cutils.progressbar_free(self._pb) 

	def __enter__(self): 
		return self 

	def __exit__(self, exc_type, exc_value, exc_tb): 
		self.finish() 
		return exc_value is None 

	@property 
	def maxval(self): 
		r""" 
		**VICE Developer's Documentation** 

		Type : ``int`` [positive definite] 

		The maximum number of iterations in the progressbar. 
		""" 
		return self._pb[0].maxval 

	@maxval.setter 
	def maxval(self, value): 
		if isinstance(value, numbers.Number): 
			if value % 1 == 0: 
				if value > 0: 
					self._pb[0].maxval = <unsigned long> value 
				else: 
					raise ValueError("""\
Attribute 'maxval' must be positive. Got: %d""" % (value)) 
			else: 
				raise ValueError("""\
Attribute 'maxval' must be an integer. Got: %g""" % (value)) 
		else: 
			raise TypeError("""\
Attribute 'maxval' must be an integer. Got: %s""" % (type(value))) 

	@property 
	def left_hand_side(self): 
		r""" 
		**VICE Developer's Documentation** 

		Type : ``str`` 

		The string that will print on the left hand side of the progressbar. 
		Defaults to the current and maximum number of iterations. 
		""" 
		return "".join([chr(self._pb[0].left_hand_side[i]) for i in range(
			strlen(self._pb[0].left_hand_side))]) 

	@left_hand_side.setter 
	def left_hand_side(self, value): 
		if isinstance(value, strcomp): 
			_cutils.progressbar_set_left_hand_side(self._pb, 
				value.encode("latin-1")) 
		else: 
			raise TypeError("""Attribute 'left_hand_side' must be of type str. \
Got: %s""" % (type(value))) 

	@property 
	def right_hand_side(self): 
		r""" 
		**VICE Developer's Documentation** 

		Type : ``str`` 

		The string that will print on the right hand side of the progressbar. 
		Defaults to an ETA on the time remaining for the calculation. 
		""" 
		return "".join([chr(self._pb[0].right_hand_side[i]) for i in range(
			strlen(self._pb[0].right_hand_side))]) 

	@right_hand_side.setter 
	def right_hand_side(self, value): 
		if isinstance(value, strcomp): 
			_cutils.progressbar_set_right_hand_side(self._pb, 
				value.encode("latin-1")) 
		else: 
			raise TypeError("""Attribute 'right_hand_side' must be of type \
str. Got: %s""" % (type(value))) 

	def finish(self): 
		r""" 
		**VICE Developer's Documentation** 

		Finish the progressbar by placing the current number of iterations at 
		self.maxval and moving to a new line in the terminal output. 

		**Signature**: x.finish() 

		Parameters 
		----------
		x : ``progressbar`` 
			An instance of this class. 
		""" 
		_cutils.progressbar_finish(self._pb) 

	def update(self, value): 
		r""" 
		**VICE Developer's Documentation** 

		Update the progressbar with a new number of iterations. 

		**Signature**: x.update(value) 

		Parameters 
		----------
		x : ``progressbar`` 
			An instance of this class. 
		value : ``int`` 
			An integer between 0 and x.maxval. 
		""" 
		if isinstance(value, numbers.Number): 
			if value % 1 == 0: 
				if 0 <= value <= self.maxval: 
					_cutils.progressbar_update(self._pb, <unsigned long> value) 
				else: 
					raise ValueError("""\
Value out of bounds for progressbar of maximum value %d: %d""" % (
						self.maxval, value)) 
			else: 
				raise ValueError("Value must be an integer. Got: %g" % (value)) 
		else: 
			raise TypeError("Value must be an integer. Got: %s" % (
				type(value))) 


cdef void callback_1arg_setup(CALLBACK_1ARG *cb1, value) except *: 
	r""" 
	Setup a callback object for a python function. 

	.. note:: This function assumed memory has already been allocated. 

	Parameters 
	----------
	cb1 : CALLBACK_1ARG * 
		A pointer to the callback object for the function 
	value : <function> or real number 
		The python function to get a callback object for. This must accept 
		exactly one positional argument if callable, as the name of the object 
		suggests, and is assumed to already be wrapped by one of the callback1 
		classes. If a real number, a function is still assigned to one that 
		always evaluates to that value.  

	Raises 
	------
	* TypeError 
		-	``value`` is neither a number nor callable 
		-	``value`` is callable and does not accept exactly one positional 
			argument 
			
	.. seealso:: vice/core/callback.py 
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


cdef void callback_2arg_setup(CALLBACK_2ARG *cb2, value) except *: 
	r""" 
	Setup a callback object for a python function. 

	.. note:: This function assumed memory has already been allocated. 

	Parameters 
	----------
	cb2 : CALLBACK_2ARG * 
		A pointer to the callback object for the function 
	value : <function> or real number 
		The python function to get a callback object for. This must accept 
		exactly two positional arguments if callable, as the name of the 
		object suggests, and is assumed to already be wrapped by one of the 
		callback2 classes. If a real number, a function is still assigned to 
		one that always evaluates to that value. 

	Raises 
	------
	* TypeError 
		-	``value`` is neither a number nor callable 
		-	``value`` is callable and does not accept exactly two positional 
			arguments 

	.. seealso:: vice/core/callback.py 
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


cdef double callback_1arg(double x, void *f): 
	r""" 
	Call a function of one numerical value defined in Python from C. 

	Parameters 
	----------
	x : real number 
		The value to evaluate the function at. Called under the hood in C, this 
		will always be a real number. 
	f : <function> 
		A void pointer to the PyObject corresponding to the user's function 
		which they've defined in python 

	Returns 
	-------
	result : real number 
		f(x), if the function returns a numerical value. If the value is 
		non-numerical, a value of 0 will be assumed. 

	Raises 
	------
	* ScienceWarning 
		-	A non-numerical value is returned from the function, forcing it to 
			assume a default value of zero. 

	.. seealso:: vice/core/callback.py 
	""" 
	# pythonic callback objects handle errors 
	return <double> (<object> f)(x) 


cdef double callback_2arg(double x, double y, void *f): 
	r""" 
	Call a function of two numerical values defined in Python from C. 

	Parameters 
	----------
	x : real number 
		The first numerical argument to the function. 
	y : real number 
		The second numerical argument to the function. 
	f : <function> 
		A void pointer to the PyOjbect corresponding to the user's function 
		which they've defined in python. 

	Returns 
	-------
	result : real number 
		f(x, y), if the function returns a numerical value. If the value is 
		non-numerical, a value of 0 will be assumed. 

	Raises 
	------
	* ScienceWarning 
		-	A non-numerical value is returned from the function, forcing it to 
			assume a default value of zero. 

	.. seealso:: vice/core/callback.py 
	""" 
	# pythonic callback objects handle errors 
	return <double> (<object> f)(x, y) 


cdef void setup_imf(IMF_ *imf, IMF) except *: 
	r""" 
	Setup an IMF_ object. 

	.. note:: This function assumed memory has already been allocated. 

	Parameters 
	----------
	imf : IMF_ *
		A pointer to the IMF_ object 
	IMF : str [case-insensitive] or <function> 
		The user's IMF prescription - either a string denoting a built-in IMF 
		or a callback object associated with a custom IMF constructed by the 
		user. 

	Raises 
	------
	* TypeError 
		- IMF is neither a string nor a function 
	* ValueError 
		- A string is not recognized as a built-in IMF 

	.. seealso:: vice/core/callback.py 
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


cdef void set_string(char *dest, pystr) except *: 
	r""" 
	Sets a string value (char *) given the python string it should be 
	set to. 

	Parameters 
	----------
	dest : char * 
		The char pointer to put the copy of the python string into 
	pystr : str 
		The python string to copy into C 

	Notes 
	-----
	This implementation simply converts the python string to ordinal numbers, 
	copies them in C, in which the set_char_p_value function sets a '\0' 
	null terminator at the end. 

	.. seealso:: vice/src/utils.h 
	""" 
	if not _pyutils.is_ascii(pystr): 
		raise ValueError("Must be ascii string.") 
	else: 
		pass 
	cdef int *ords = ordinals(pystr) 
	set_char_p_value(dest, ords, len(pystr)) 
	free(ords) 


cdef int *ordinals(pystr) except *: 
	r""" 
	Obtain an int* of the ascii indeces of the characters in a string. 

	Parameters 
	----------
	pystr : str 
		An ascii python string. 

	Returns 
	------- 
	A C char * with the same contents as pystr. 

	Raises 
	------
	* TypeError 
		- ``pystr`` is not a python string 
	""" 
	if not isinstance(pystr, strcomp): 
		raise TypeError("Must be of type str. Got: %s" % (type(pystr))) 
	else: 
		pass 

	cdef int *copy = <int *> malloc (len(pystr) * sizeof(int)) 
	for i in range(len(pystr)): 
		copy[i] = ord(pystr[i]) 
	return copy 


cdef double *copy_pylist(pylist) except *: 
	r"""
	Allocate memory for a double pointer and copy each element of a python 
	list into the resultant C array. 

	Parameters 
	----------
	pylist : array-like 
		A python 1D array-like object than can be indexed via pylist[x] 

	Raises 
	------
	* TypeError 
		- ``pylist`` has a non-numerical value 
	""" 
	cdef double *copy = <double *> malloc (len(pylist) * sizeof(double)) 
	for i in range(len(pylist)): 
		if isinstance(pylist[i], numbers.Number): 
			copy[i] = pylist[i] 
		else: 
			free(copy) 
			raise TypeError("Non-numerical value detected.") 
	return copy 
	

cdef double **copy_2Dpylist(pylist) except *: 
	r""" 
	Allocate memory for a 2-D double pointer array and copy each element of a 
	python list into the resultant C array. 

	Parameters 
	----------
	pylist : array-like 
		A python 2D array-like object that can be indexed via pylist[x][y] 

	Raises 
	------
	* TypeError 
		- pylist has a non-numerical value 
	""" 
	cdef double **copy = <double **> malloc (len(pylist) * sizeof(double *)) 
	for i in range(len(pylist)): 
		copy[i] = <double *> malloc (len(pylist[i]) * sizeof(double)) 
		for j in range(len(pylist[i])): 
			if isinstance(pylist[i][j], numbers.Number): 
				copy[i][j] = pylist[i][j] 
			else: 
				free(copy) 
				raise TypeError("Non-numerical value detected.") 
	return copy 


cdef double *map_pyfunc_over_array(pyfunc, pyarray) except *: 
	r"""
	Map a python function across an array of values and store the output in 
	a double pointer. 

	Parameters 
	----------
	pyfunc : <function> 
		The function to map. Must take only one parameter (i.e. pyfunc(x)) 
	pyarray : array-like 
		The array to map pyfunc over. Must be 1D and taking only numerical 
		values. 

	Returns 
	-------
	mapped : double * 
		The double pointer to the C array containing the mapped values 

	Raises 
	------
	* TypeError 
		- ``pyarray`` contains a non-numerical value 
		- ``pyfunc`` maps to a non-numerical value 
		- ``pyfunc`` is not callable 
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
				free(mapped) 
				raise TypeError("Function mapped to non-numerical value.") 
		else: 
			raise TypeError("Non-numerical value detected.") 
	return mapped  

