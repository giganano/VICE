
from __future__ import division 
from .._globals import _VERSION_ERROR_ 
try: 
	ModuleNotFoundError 
except NameError: 
	ModuleNotFoundError = ImportError 
try: 
	# NumPy compatible but not NumPy dependent 
	import numpy as np 
except (ModuleNotFoundError, ImportError): 
	pass 
try: 
	# Pandas compatible but not Pandas dependent 
	import pandas as pd 
except (ModuleNotFoundError, ImportError): 
	pass 
import math as m 
import numbers 
import warnings 
import array 
import sys 
import os 
if sys.version_info[:2] == (2, 7): 
	strcomp = basestring 
elif sys.version_info[:2] >= (3, 5): 
	strcomp = str 
else: 
	_VERSION_ERROR_() 

def numeric_check(pylist, errtype, errmsg): 
	"""
	Raises an exception if any elements of a python array-like object are 
	non-numerical. 

	Parameters 
	========== 
	pylist :: array-like 
		A python array-like object 
	errtype :: Exception 
		The exception type to raise in the event of non-numerical value 
	errmsg :: string 
		The error message to print in the case of non-numerical values 

	Raises 
	====== 
	errtype :: 
		:: at least one element of pylist is non-numerical 
	"""
	copy = copy_array_like_object(pylist) 
	if any(list(map(lambda x: not isinstance(x, numbers.Number), copy))): 
		raise errtype(errmsg) 
	else: 
		pass 

def inf_nan_check(pylist, errtype, errmsg): 
	""" 
	Raises an exception if any elements of a python array-like object are 
	non-numerical. 

	Parameters 
	========== 
	pylist :: list 
		A python list of numerical values 
	errtype :: Exception 
		The exception type to raise in the event of infs or nans 
	errmsg :: string 
		The error message to print in the case of infs or nans 

	Raises 
	====== 
	errtype :: 
		:: at least one element of pylist is an inf or nan 

	Notes 
	===== 
	In practice, this function should be called AFTER numeric_check 
	""" 
	assert all(map(lambda x: isinstance(x, numbers.Number), pylist)) 
	if any(map(lambda x: m.isnan(x) or m.isinf(x), pylist)): 
		raise errtype(errmsg) 
	else: 
		pass 

def copy_array_like_object(pyobj): 
	"""
	Pull a copy of an array-like object. 

	Parameters 
	========== 
	pyobj :: array-like 
		Some python array-like object 

	Returns 
	======= 
	The same object as a list 

	Raises 
	====== 
	TypeError :: 
		:: pyobj is not array-like 
	""" 
	if isinstance(pyobj, array.array): 
		# native python array 
		copy = pyobj.tolist() 
	elif "numpy" in sys.modules and isinstance(pyobj, np.ndarray): 
		# pyobj is a numpy array 
		copy = pyobj.tolist() 
	elif "pandas" in sys.modules and isinstance(pyobj, pd.DataFrame): 
		# copy is a pandas DataFrame 
		copy = [i[0] for i in pyobj.values.tolist()] 
	elif type(pyobj) in [list, tuple]: 
		copy = pyobj[:] 
	else: 
		raise TypeError("Must be an array-like object. Got: %s" % (
			type(pyobj)))

	return copy 

def range_(start, stop, dx): 
	"""
	A replacement to numpy.linspace and native python range() 

	Parameters 
	========== 
	start :: real number
		The first element of the returned list 
	stop :: real number 
		The final element of the returned list 
	dx :: real number 
		The step size to take between 0 and this element 

	Returns 
	======= 
	A python list whose first element is start and final element is stop 
	with intermediate elements spaced linearly by dx 

	Raises 
	====== 
	TypeError :: 
		:: start is not a numerical value 
		:: stop is not a numerical value 
		:: dx is non a numerica value 
	""" 
	if not isinstance(start, numbers.Number): 
		raise TypeError("Must be a numerical value. Got: %s" % (type(start))) 
	elif not isinstance(stop, numbers.Number): 
		raise TypeError("Must be a numerical value. Got: %s" % (type(stop))) 
	elif not isinstance(dx, numbers.Number): 
		raise TypeError("Must be a numerical value. Got: %s" % (type(dx))) 
	else: 
		arr = int(((stop - start) / dx) + 1) * [0.] 
		for i in range(len(arr)): 
			arr[i] = start + i * dx 
		return arr 

def args(func, errmsg): 
	"""
	Raises a TypeError if the function accepts any more than one positional 
	parameter, or if that positional parameter is non-numerical. 

	Parameters 
	========== 
	func :: callable 
		python function 
	errmsg :: string 
		The error message to print if func fails the test. 

	Raises 
	====== 
	TypeError :: 
		:: func can't evaluate with only one positional numerical value 
	"""
	if callable(func): 
		try: 
			foo = func(1) 
		except TypeError: 
			raise TypeError(errmsg) 
	else: 
		raise TypeError("Must be a callable python function. Got: %s" % (
			type(func))) 

def is_ascii(pystr): 
	""" 
	Returns true if all characters in a string are ascii. 

	Parameters 
	========== 
	pystr :: str 
		The python string itself 
	""" 
	if isinstance(pystr, strcomp): 
		return all([ord(c) < 128 for c in pystr]) 
	else: 
		raise TypeError("Must be of type str. Got: %s" % (type(pystr))) 







