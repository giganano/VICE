r"""
Python Utilities
================

.. warning:: User access of this module is discouraged

Contains under-the-hood utility functions for VICE's python side.
"""

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
import inspect
import numbers
import array
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


def numeric_check(pylist, errtype, errmsg):
	r"""
	Raises an exception if any elements of a python array-like object are
	non-numerical.

	Parameters
	----------
	pylist : array-like
		A python array-like object
	errtype : Exception
		The exception type to raise in the event of non-numerical value
	errmsg : str
		The error message to print in the case of non-numerical values

	Raises
	------
	* errtype
		- At least one element of pylist is non-numerical
	"""
	copy = copy_array_like_object(pylist)
	if any(list(map(lambda x: not isinstance(x, numbers.Number), copy))):
		raise errtype(errmsg)
	else:
		pass


def inf_nan_check(pylist, errtype, errmsg):
	r"""
	Raises an exception if any elements of a python array-like object are
	non-numerical.

	Parameters
	----------
	pylist : list
		A python list of numerical values
	errtype : Exception
		The exception type to raise in the event of infs or nans
	errmsg : str
		The error message to print in the case of infs or nans

	Raises
	------
	* errtype
		- At least one element of pylist is an inf or nan

	Notes
	-----
	In practice, this function should be called AFTER numeric_check
	"""
	assert all(map(lambda x: isinstance(x, numbers.Number), pylist))
	if any(map(lambda x: m.isnan(x) or m.isinf(x), pylist)):
		raise errtype(errmsg)
	else:
		pass


def copy_array_like_object(pyobj):
	r"""
	Pull a copy of an array-like object.

	Parameters
	----------
	pyobj : array-like
		Some python array-like object

	Returns
	-------
	copy : list
		``pyobj`` copied to a list

	Raises
	------
	* TypeError
		- ``pyobj`` is not array-like
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
	r"""
	A replacement to numpy.arange and native python range()

	Parameters
	----------
	start : real number
		The first element of the returned list
	stop : real number
		The final element of the returned list
	dx : real number
		The step size to take between 0 and this element

	Returns
	-------
	x : list
		A list whose first element is start and final element is stop
		with intermediate elements spaced linearly by dx

	Raises
	------
	* TypeError
		- ``start`` is not a numerical value
		- ``stop`` is not a numerical value
		- ``dx`` is non a numerica value
	"""
	if not isinstance(start, numbers.Number):
		raise TypeError("Must be a numerical value. Got: %s" % (type(start)))
	elif not isinstance(stop, numbers.Number):
		raise TypeError("Must be a numerical value. Got: %s" % (type(stop)))
	elif not isinstance(dx, numbers.Number):
		raise TypeError("Must be a numerical value. Got: %s" % (type(dx)))
	else:
		r"""
		Use recursion to force the algorithm to always run in increasing order
		with a positive dx.
		"""
		if dx < 0:
			return range_(start, stop, -dx)
		elif stop < start:
			return range_(stop, start, dx)
		elif stop == start:
			return [start]
		else:
			r"""
			Using an append approach causes floating point round-off errors
			here, causing the test to fail
			"""
			arr = int(((stop - start) / dx) + 1) * [0.]
			for i in range(len(arr)):
				arr[i] = start + i * dx
			if arr[-1] < stop: arr.append(len(arr) * dx)
			return arr

def args(func, errmsg):
	r"""
	Raises a TypeError if the function accepts any more than one positional
	parameter, or if that positional parameter is non-numerical.

	Parameters
	----------
	func : callable
		A callable object (usually a function).
	errmsg : string
		The error message to print if ``func`` fails the test.

	Raises
	------
	* TypeError
		- ``func`` can't evaluate with only one positional numerical value

	Notes
	-----
	This function does a simple try-except statement, calling the function
	with a value of 1. This is required because a simple argument count does
	not suffice; this is intended to make sure that functions accept
	**numerical** parameters specifically.
	"""
	if callable(func):
		try:
			foo = func(1)
		except TypeError:
			raise TypeError(errmsg)
	else:
		raise TypeError("Must be a callable python function. Got: %s" % (
			type(func)))


def arg_count(func):
	r"""
	Determine the number of positional arguments accepted by a given python
	function.

	Parameters
	----------
	func :: callable
		A callable object (usually a function).

	Returns
	-------
	n : int
		The number of parameters to the function that do not accept a default
		value.

	Raises
	------
	* TypeError
		- ``func`` is not callable
	"""
	if callable(func):
		n = 0
		sig = inspect.signature(func)
		for i in sig.parameters.keys():
			n += int(sig.parameters[i].default == inspect._empty)
		return n
	else:
		raise TypeError("Must be a callable object. Got: %s" % (type(func)))


def is_ascii(pystr):
	r"""
	Determine if a string is made of entirely ascii characters.

	Parameters
	----------
	pystr : str
		The python string itself

	Returns
	-------
	is_ascii : bool
		True if ``pystr`` is made entirely of ascii characters; False
		otherwise.

	Raises
	------
	* TypeError
		- ``pystr`` is not a string.
	"""
	if isinstance(pystr, strcomp):
		return all([ord(c) < 128 for c in pystr])
	else:
		raise TypeError("Must be of type str. Got: %s" % (type(pystr)))


def format_time(seconds):
	r"""
	Convert a time in seconds into days, hours, minutes, and seconds.

	Parameters
	----------
	seconds : float
		An amount of time in seconds.

	Returns
	-------
	days : int
		The number of days in the specified time interval.
	hours : int
		The number of hours in excess of the number of days.
	minutes : int
		The number of minutes in excess of the number of hours.
	seconds : int
		The number of seconds in excess of the number of minutes.
	"""
	if isinstance(seconds, numbers.Number):
		days = seconds // (24 * 3600)
		seconds %= 24 * 3600
		hours = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		return [int(days), int(hours), int(minutes), int(seconds)]
	else:
		raise TypeError("Must be a real number. Got: %s" % (type(seconds)))

