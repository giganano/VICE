# cython: language_level = 3, boundscheck = False
"""
This file handles the implementation of the base class of the VICE dataframe.
The most distinguishing feature of the VICE dataframe from other dataframes
such as that of Pandas is that the VICE dataframe is case-insensitive, while
retaining the ability to index based on either column label or row number.
"""

from __future__ import absolute_import
from ..._globals import _VERSION_ERROR_
from .. import _pyutils
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _base


#------------------------- VICE DATAFRAME BASE CLASS -------------------------#
cdef class base:

	r"""
	The VICE Dataframe: base class

	Provides a means of storing and accessing data with both case-insensitive
	strings and integers, allowing both indexing and calling.

	**Signature**: vice.dataframe(frame)

	Parameters
	----------
	frame : ``dict``
		A python dictionary to construct the dataframe from. Keys must all
		be of type ``str``.

	Raises
	------
	* TypeError
		- frame has a key that is not of type ``str``

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : column label
			A label given to the stored quantity (or list/array thereof).

	* Values
		- All

	Indexing
	--------
	- ``str`` [case-insensitive] : column label
		A label given to the quantities stored.
	- ``int`` : index for values which are array-like.
		If all values stored by the dataframe are array-like, the i'th value
		of all of them can be obtained by indexing the dataframe with ``i``.

	Calling
	-------
	The VICE dataframe and all subclasses can be called rather than indexed
	to achieve the same result.

	Functions
	---------
	- keys
	- todict
	- remove
	- filter

	Example Code
	------------
	>>> import vice
	>>> example = vice.dataframe({
		"a": [1, 2, 3],
		"b": [4, 5, 6],
		"c": [7, 8, 9]})
	>>> example["A"]
	[1, 2, 3]
	>>> example("a")
	[1, 2, 3]
	>>> example[0]
	vice.dataframe{
		a --------------> 1
		b --------------> 4
		c --------------> 7
	}
	>>> example.keys()
	['a', 'b', 'c']
	>>> example.todict()
	{'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
	>>> example.filter("c", "<", 9)
	vice.dataframe{
		a --------------> [1, 2]
		b --------------> [4, 5]
		c --------------> [7, 8]
	}
	"""

	# cdef object _frame

	def __init__(self, frame):
		if isinstance(frame, dict):
			if all(map(lambda x: isinstance(x, strcomp), frame.keys())):
				keys = tuple([i.lower() for i in frame.keys()])
				values = tuple([frame[i] for i in frame.keys()])
				self._frame = dict(zip(keys, values))
			else:
				raise TypeError("All keys must be of type str.")
		else:
			raise TypeError("""Can only initialize dataframe from type dict. \
Got: %s""" % (type(frame)))


	def __call__(self, key):
		"""
		Return the same thing as __getitem__.
		"""
		return self.__getitem__(key)


	def __getitem__(self, key):
		"""
		If type str, index the dataframe on key.lower(). This allows
		case-insensitivity. If an integer, will attempt to pull the proper
		row from a dataframe containing array-like attributes.

		In this case, the returned value will also be a dataframe.
		"""
		if isinstance(key, strcomp): # index via column label
			return self.__subget__str(key)
		elif isinstance(key, numbers.Number): # index via row number
			return self.__subget__number(key)
		else:
			raise IndexError("""Only integers and strings are valid indeces. \
Got: %s""" % (type(key)))


	def __subget__str(self, key):
		"""
		Performs the __getitem__ operation when the key is a string.
		"""
		if key.lower() in self.keys():
			return self._frame[key.lower()]
		else:
			raise KeyError("Unrecognized dataframe key: %s" % (key))


	def __subget__number(self, key):
		"""
		Performs the __getitem__ operation when the key is a number
		"""
		if key % 1 == 0:
			# index by int only works when all fields are array-like
			if all(map(lambda x: hasattr(self._frame[x], "__getitem__"),
				self.keys())):
				try:
					x = [self._frame[i][int(key)] for i in self.keys()]
					return base(dict(zip(
						self.keys(),
						x
					)))
				except IndexError:
					raise IndexError("Index out of bounds: %d" % (int(key)))
				except Exception as exc:
					msg = """\
The following exception occurred when indexing dataframe with key: %d

%s""" % (int(key), exc.args[0])
					exc.args = (msg,)
					raise
			else:
				raise IndexError("""Cannot index with key of type int: not \
all values array-like.""")
		else:
			raise IndexError("""Index must be interpreted as an integer. \
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


	def __hash__(self):
		return id(self)


	def keys(self):
		r"""
		Returns the keys to the dataframe in their lower-case format

		**Signature**: x.keys()

		Parameters
		----------
		x : ``dataframe``
			An instance of this class

		Returns
		-------
		keys : ``list``
			A list of lower-case strings which can be used to access the
			values stored in this dataframe.

		Example Code
		------------
		>>> import vice
		>>> example = vice.dataframe({
			"a": [1, 2, 3],
			"b": [4, 5, 6],
			"c": [7, 8, 9]})
		>>> example
		vice.dataframe{
			a --------------> [1, 2, 3]
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.keys()
		['a', 'b', 'c']
		"""
		return [i.lower() for i in self._frame.keys()]


	def todict(self):
		r"""
		Returns the dataframe as a standard python dictionary

		**Signature**: x.todict()

		Parameters
		----------
		x : ``dataframe``
			An instance of this class

		Returns
		-------
		copy : ``dict``
			A dictionary copy of the dataframe.

		.. note:: Python dictionaries are case-sensitive, and are thus less
			flexible than this class.

		Example Code
		------------
		>>> import vice
		>>> example = vice.dataframe({
			"a": [1, 2, 3],
			"b": [4, 5, 6],
			"c": [7, 8, 9]})
		>>> example
		vice.dataframe{
			a --------------> [1, 2, 3]
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.todict()
		{'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
		"""
		return self._frame.copy()


	def remove(self, key):
		r"""
		Remove an element of the dataframe

		**Signature**: x.remove(key)

		.. versionadded:: 1.1.0

		Parameters
		----------
		x : ``dataframe``
			An instance of this class
		key : ``str`` [case-insensitive]
			The key to remove from the dataframe

		Raises
		------
		* KeyError
			- Key is not in the dataframe

		Example Code
		------------
		>>> import vice
		>>> example = vice.dataframe({
			"a": [1, 2, 3],
			"b": [4, 5, 6],
			"c": [7, 8, 9]})
		>>> example
		vice.dataframe{
			a --------------> [1, 2, 3]
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.remove("a")
		vice.dataframe{
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.remove("b")
		vice.dataframe{
			c --------------> [7, 8, 9]
		}
		"""
		if key.lower() in self._frame.keys():
			del self._frame[key.lower()]
		else:
			raise KeyError("Unrecognized dataframe key: %s" % (key))


	def filter(self, key, relation, value):
		r"""
		Obtain a copy of the dataframe whose elements satisfy a filter. Only
		applies to dataframes whose values are all array-like.

		**Signature**: x.filter(key, relation, value)

		.. versionadded:: 1.1.0

		Parameters
		----------
		x : ``dataframe``
			An instance of this class
		key : ``str`` [case-insensitive]
			The dataframe key to filter based on
		relation : ``str``
			Either '<', '<=', '=', '==', '!=', '>=', or '>', denoting the
			relation to filter based on.
		value : real number
			The value to filter based on.

		Returns
		-------
		filtered : ``dataframe``
			A dataframe whose elements are only those which satisfy the
			specified filter. This will always be an instance of the base
			class, even if the function called with an instance of a derived
			class.

		Raises
		------
		* KeyError
			- Key is not in the dataframe
		* ValueError
			- Invalid relation

		Example Code
		------------
		>>> import vice
		>>> example = vice.dataframe({
			"a": [1, 2, 3],
			"b": [4, 5, 6],
			"c": [7, 8, 9]})
		>>> example
		vice.dataframe{
			a --------------> [1, 2, 3]
			b --------------> [4, 5, 6]
			c --------------> [7, 8, 9]
		}
		>>> example.filter("a", "=", 2)
		vice.dataframe{
			a --------------> [2]
			b --------------> [5]
			c --------------> [8]
		}
		>>> example.filter("c", "<=", 8)
		vice.dataframe{
			a --------------> [1, 2]
			b --------------> [4, 5]
			c --------------> [7, 8]
		}
		"""
		if isinstance(key, strcomp):
			if key.lower() in self.keys():
				if isinstance(value, numbers.Number):
					idx = self.keys().index(key.lower())
					qtys = [self.__getitem__(i) for i in self.keys()]
					if any(map(lambda x: not hasattr(x, "__getitem__"), qtys)):
						raise TypeError("""Filter function not allowed: not \
all values array-like.""")
					else: pass
					copy = len(qtys[0]) * [None]
					for i in range(len(copy)):
						copy[i] = [row[i] for row in qtys]

					if relation == '<':
						fltrd = list(filter(lambda x: x[idx] < value, copy))
					elif relation == '<=':
						fltrd = list(filter(lambda x: x[idx] <= value, copy))
					elif relation == '=' or relation == '==':
						fltrd = list(filter(lambda x: x[idx] == value, copy))
					elif relation == '!=':
						fltrd = list(filter(lambda x: x[idx] != value, copy))
					elif relation == '>=':
						fltrd = list(filter(lambda x: x[idx] >= value, copy))
					elif relation == '>':
						fltrd = list(filter(lambda x: x[idx] > value, copy))
					else:
						raise ValueError("Invalid relation: %s" % (
							str(relation)))

					new = {}
					for i in range(len(self.keys())):
						new[self.keys()[i]] = [row[i] for row in fltrd]

					return base(new)

				else:
					raise TypeError("Value must be a real number. Got: %s" % (
						type(value)))
			else:
				raise KeyError("Invalid dataframe key: %s" % (key))
		else:
			raise KeyError("Key must be of type str for filter. Got: %s" % (
				type(key)))

