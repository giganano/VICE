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
from .singlezone._imf cimport IMF_ 
from .singlezone._agb cimport AGB_YIELD_GRID 
from .singlezone cimport _agb 
from .singlezone cimport _ccsne 
from .singlezone cimport _sneia 

cdef extern from "../src/utils.h": 
	double *binspace(double start, double stop, long N) 
	void set_char_p_value(char *dest, int *ords, int length) 

cdef extern from "../src/imf.h": 
	double IMF_STEPSIZE 
	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 

cdef extern from "../src/objects.h": 
	ctypedef struct CALLBACK_1ARG: 
		double (*callback)(double, void *) 
		void *user_func 

	ctypedef struct CALLBACK_2ARG: 
		double (*callback)(double, double, void *) 
		void *user_func 

	CALLBACK_1ARG *callback_1arg_initialize() 
	void callback_1arg_free(CALLBACK_1ARG *cb1) 

	CALLBACK_2ARG *callback_2arg_initialize() 
	void callback_2arg_free(CALLBACK_2ARG *cb2) 


cdef inline CALLBACK_1ARG *callback_1arg_from_pyfunc(pyfunc) except *: 
	""" 
	Get a callback object for a python function 

	Parameters 
	========== 
	pyfunc :: <function> 
		The python function to get a callback object for. This must accept 
		exactly one positional argument, as the name of the object suggests. 

	Returns 
	======= 
	cb1 :: CALLBACK_1ARG * 
		A pointer to the callback object for the function 

	Raises 
	====== 
	TypeError :: 
		::	pyfunc is not a callable object 
		::	pyfunc does not accept exactly one positional argument 
	""" 
	cdef CALLBACK_1ARG *cb1 
	if callable(pyfunc): 
		if _pyutils.arg_count(pyfunc) == 1: 
			cb1 = callback_1arg_initialize() 
			cb1[0].callback = &callback_1arg 
			cb1[0].user_func = <void *> pyfunc 
			return cb1 
		else: 
			raise TypeError("""Function must accept exactly one positional \
argument.""") 
	else: 
		raise TypeError("Function must be a callable object. Got: %s" % (
			type(pyfunc))) 


cdef inline CALLBACK_2ARG *callback_2arg_from_pyfunc(pyfunc) except *: 
	""" 
	Get a callback object for a python function 

	Parameters 
	========== 
	pyfunc :: <function> 
		The python function to get a callback object for. This must accept 
		exactly two positional arguments, as the name of the object suggests. 

	Returns 
	======= 
	cb2 :: CALLBACK_2ARG * 
		A pointer to the callback object for the function 

	Raises 
	====== 
	TypeError :: 
		::	pyfunc is not a callable object 
		::	pyfunc does not accept exactly two positional arguments 
	""" 
	cdef CALLBACK_2ARG *cb2 
	if callable(pyfunc): 
		if _pyutils.arg_count(pyfunc) == 2: 
			cb2 = callback_2arg_initialize() 
			cb2[0].callback = &callback_2arg 
			cb2[0].user_func = <void *> pyfunc 
			return cb2 
		else: 
			raise TypeError("""Function must accept exactly two positional \
arguments.""") 
	else: 
		raise TypeError("Function must be a callable object. Got: %s" % (
			type(pyfunc))) 


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
	""" 
	result = (<object> f)(x) 
	if isinstance(result, numbers.Number): 
		return <double> result 
	else: 
		warnings.warn("""Function %s evaluated at %s returned a non-numerical \
value: %s. This calculation will proceed with a default value of zero.""" % (
			str(<object> f), str(x), str(result)), ScienceWarning) 
		return 0.0 


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
	""" 
	result = (<object> f)(x, y) 
	if isinstance(result, numbers.Number): 
		return <double> result 
	else: 
		warnings.warn("""Function %s evaluated at (%s, %s) returned a \
non-numerical value: %s. This calculation will proceed with a default value of \
zero.""" % (str(<object> f), str(x), str(y), str(result)), ScienceWarning) 
		return 0.0 


# cdef inline CALLBACK_1ARG *setup_ccsne_yield(element) except *: 
# 	""" 
# 	Sets up a callback object according to the user's current CCSN yield 
# 	setting. 

# 	Parameters 
# 	========== 
# 	element :: str [case-insensitive] 
# 		The element to setup the callback object for 

# 	Raises 
# 	====== 
# 	TypeError :: 
# 		::	The element's yield setting is neither a number nor a function. 
# 			This should only happen if the user has hacked VICE's source code. 
# 	""" 
# 	def yieldfunc(Z): 
# 		if callable(ccsne.settings[element]): 
# 			return ccsne.settings[element](Z) 
# 		else: 
# 			return ccsne.settings[element] 
# 	return callback_1arg_from_pyfunc(yieldfunc) 
	# cdef CALLBACK_1ARG *cb1 
	# if callable(ccsne.settings[element]): 
	# 	yieldfunc = ccsne.settings[element] 
	# else: 
	# 	def yieldfunc(Z): 
	# 		return ccsne.settings[element](Z) 
	# cb1 = callback_1arg_from_pyfunc(yieldfunc) 
	# return cb1 


# cdef inline object map_ccsne_yield(element): 
# 	""" 
# 	Maps the user's current CCSN yield setting across the yield array defined 
# 	by CC_YIELD_GRID_MIN, CC_YIELD_GRID_MAX, and CC_YIELD_STEP. 

# 	Parameters 
# 	========== 
# 	element :: str [case-insensitive] 
# 		The element to map the yield for. 
# 	""" 
# 	ccyield = ccsne.settings[element] 
# 	if callable(ccyield): 
# 		# each line ensures basic requirements of the yield settings 
# 		_pyutils.args(ccyield, """Yields from core-collapse supernovae, when \
# callable, must take only one numerical parameter.""") 
# 		z_arr = _pyutils.range_(_ccsne.CC_YIELD_GRID_MIN, 
# 			_ccsne.CC_YIELD_GRID_MAX, 
# 			_ccsne.CC_YIELD_STEP 
# 		) 
# 		arr = list(map(ccyield, z_arr)) 
# 		_pyutils.numeric_check(arr, ArithmeticError, """Yield as a function \
# of metallicity mapped to non-numerical value.""") 
# 		_pyutils.inf_nan_check(arr, ArithmeticError, """Yield as a function \
# of metallicity mapped to NaN or inf for at least one metallicity.""") 
# 		return arr 
# 	elif isinstance(ccyield, numbers.Number): 
# 		if m.isinf(ccyield) or m.isnan(ccyield): 
# 			raise ArithmeticError("Yield cannot be inf or NaN.") 
# 		else: 
# 			return len(_pyutils.range_(_ccsne.CC_YIELD_GRID_MIN, 
# 				_ccsne.CC_YIELD_GRID_MAX, 
# 				_ccsne.CC_YIELD_STEP
# 			)) * [ccyield] 
# 	else: 
# 		raise TypeError("""IMF-integrated yield from core collapse \
# supernovae must be either a numerical value or a function of metallicity. \
# Got: %s""" % (type(ccyield))) 


# cdef inline CALLBACK_1ARG *setup_sneia_yield(element) except *: 
# 	""" 
# 	Sets up a callback object according to the user's current SN Ia yield 
# 	setting. 

# 	Parameters 
# 	========== 
# 	element :: str [case-insensitive] 
# 		The element to setup the callback object for 

# 	Raises 
# 	====== 
# 	TypeError :: 
# 		::	The element's yield settings is neither a number nor a function. 
# 			This should only happen if the user has hacked VICE's source code. 
# 	""" 
# 	if callable(sneia.settings[element]): 
# 		yieldfunc = sneia.settings[element] 
# 	else: 
# 		def yieldfunc(Z): 
# 			return sneia.settings[element](Z) 
# 	cdef CALLBACK_1ARG *cb1 = callback_1arg_from_pyfunc(yieldfunc) 
# 	return cb1 


# cdef inline object map_sneia_yield(element): 
# 	""" 
# 	Map's the user's current SN Ia yield setting across the yield array defined 
# 	by IA_YIELD_GRID_MIN, IA_YIELD_GRID_MAX, and IA_YIELD_STEP 

# 	Parameters 
# 	========== 
# 	element :: str [case-insensitive] 
# 		The element to map the yield for 
# 	""" 
# 	iayield = sneia.settings[element] 
# 	if callable(iayield): 
# 		# each line ensures basic requirements of the yield settings 
# 		_pyutils.args(iayield, """Yields from type Ia supernovae, when \
# callable, must take only one numerical parameter.""") 
# 		z_arr = _pyutils.range_(
# 			_sneia.IA_YIELD_GRID_MIN, 
# 			_sneia.IA_YIELD_GRID_MAX, 
# 			_sneia.IA_YIELD_STEP
# 		) 
# 		arr = list(map(iayield, z_arr)) 
# 		_pyutils.numeric_check(arr, ArithmeticError, """Yield as a \
# function of metallicity mapped to non-numerical value.""") 
# 		_pyutils.inf_nan_check(arr, ArithmeticError, """Yield as a \
# function of metallicity mapped to NaN or inf for at least one metallicity.""") 
# 		return arr 
# 	elif isinstance(iayield, numbers.Number): 
# 		if m.isinf(iayield) or m.isnan(iayield): 
# 			raise ArithmeticError("Yield cannot be inf or NaN.") 
# 		else: 
# 			return len(_pyutils.range_(
# 				_sneia.IA_YIELD_GRID_MIN, 
# 				_sneia.IA_YIELD_GRID_MAX, 
# 				_sneia.IA_YIELD_STEP
# 			)) * [iayield] 
# 	else: 
# 		raise TypeError("""IMF-integrated yield from type Ia supernovae \
# must be either a numerical value or a function of metallicity. Got: %s""" % (
# 			type(iayield))) 


# cdef inline CALLBACK_2ARG *setup_agb_yield(element) except *: 
# 	""" 
# 	Sets up a callback object according to the user's current AGB star yield 
# 	setting. 

# 	Parameters 
# 	========== 
# 	element :: str [case-insensitive] 
# 		The element to setup the callback object for 

# 	Notes 
# 	===== 
# 	This function will only be called when the user has set a custom AGB star 
# 	yield. Otherwise VICE will automatically import it. 
# 	""" 
# 	return callback_2arg_from_pyfunc(agb.settings[element]) 


# cdef inline object map_agb_yield(element, masses): 
# 	""" 
# 	Maps the user's current AGB star yield setting across the 2-D yield array 
# 	defined by AGB_Z_GRID_MIN, AGB_Z_GRID_MAX, and AGB_Z_GRID_STEP 

# 	Parameters 
# 	========== 
# 	element :: str [case-insensitive] 
# 		The element to map the yield for 
# 	masses :: list 
# 		The masses resulting from calling main_sequence_turnoff_mass for all 
# 		of the times at which the simulation will evaluate. 

# 	Notes 
# 	===== 
# 	This function will only be called when the user has set a custom AGB star 
# 	yield. Otherwise VICE will automatically import it. 
# 	""" 
# 	agbyield = agb.settings[element] 
# 	z_arr = _pyutils.range_(
# 		_agb.AGB_Z_GRID_MIN, 
# 		_agb.AGB_Z_GRID_MAX, 
# 		_agb.AGB_Z_GRID_STEPSIZE 
# 	) 
# 	arr = len(masses) * [None] 
# 	for i in range(len(arr)): 
# 		arr[i] = len(z_arr) * [0.] 
# 		for j in range(len(arr[i])): 
# 			arr[i][j] = agbyield(masses[i], z_arr[j]) 
# 		_pyutils.numeric_check(arr[i], ArithmeticError, """Yield as a \
# function of mass and metallicity mapped to non-numerical value.""") 
# 		_pyutils.inf_nan_check(arr[i], ArithmeticError, """Yield as a \
# function of metallicity mapped to NaN or inf for at least one metallicity.""") 
# 	return arr 


cdef inline void setup_imf(IMF_ *imf, IMF) except *: 
	""" 
	Setup an already malloc'ed IMF_ object. 

	Parameters 
	========== 
	imf :: 	IMF_ *
		A pointer to the IMF_ object 
	IMF :: str [case-insensitive] or <function> 
		The user's IMF prescription - either a string denoting a built-in IMF 
		or a callable function denoting a custom IMF. 

	Raises 
	====== 
	TypeError :: 
		::	IMF is neither a string nor a function 
	ValueError :: 
		::	A string is not recognized as a built-in IMF 
	""" 
	if isinstance(IMF, strcomp): 
		if IMF.lower() in _RECOGNIZED_IMFS_: 
			set_string(imf[0].spec, IMF.lower()) 
		else: 
			raise ValueError("Unrecognized IMF: %s" % (IMF)) 
	elif callable(IMF): 
		imf[0].custom_imf = callback_1arg_from_pyfunc(IMF) 
		set_string(imf[0].spec, "custom") 
	else: 
		raise TypeError("""IMF must be either a string denoting a built-in \
IMF or a callable function. Got: %s""" % (type(IMF))) 

# 	cdef double *mapped 
# 	if callable(IMF): 
# 		_pyutils.args(IMF, """Stellar IMF must accept only one numerical \
# parameter.""")
# 		set_string(imf[0].spec, "custom") 
# 		masses = _pyutils.range_(imf[0].m_lower, imf[0].m_upper, IMF_STEPSIZE) 
# 		mapped = <double *> malloc (len(masses) * sizeof(double)) 
# 		for i in range(len(masses)): 
# 			mapped[i] = IMF(masses[i]) 
# 		x = imf_set_mass_distribution(imf, mapped) 
# 		free(mapped) 
# 		if x: 
# 			raise ArithmeticError("""Custom IMF evaluated to negative, inf, \
# or nan for at least one stellar mass.""") 
# 		else: pass 
# 	elif isinstance(IMF, strcomp): 
# 		if IMF.lower() in _RECOGNIZED_IMFS_: 
# 			set_string(imf[0].spec, IMF.lower()) 
# 		else: 
# 			raise ValueError("Unrecognized IMF: %s" % (IMF)) 
# 	else: 
# 		raise TypeError("""IMF must be either a string denoting a built-in \
# initial mass function or a callable function. Got: %s""" % (type(IMF))) 


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

