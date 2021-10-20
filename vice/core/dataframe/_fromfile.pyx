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
from .._cutils cimport set_string
from .._cutils cimport copy_pylist
from . cimport _fromfile


#----------------------------- FROMFILE SUBCLASS -----------------------------#
cdef class fromfile(base):

	r"""
	The VICE dataframe: derived class (inherits from base)

	Provides a means of storing and accessing generic simulation output.
	Fromfile objects are created by various functions which read in simulation
	output (e.g. vice.mdf).

	Attributes
	----------
	name : ``str``
		The name of the file that the data was pulled from.
	size : ``tuple``
		Contains two integers: the (length, width) of the data.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : the physical quantity
			A name given to the physical quantity to take from or store with
			the output.

			.. note:: VICE automatically assigns keys to quantities in the
				output which cannot be overridden.

	* Values
		- array-like
			Must have the same length as the values of the dataframe obtained
			from the output file.

	Indexing
	--------
	-	``int`` : A given line-number of the output.
		Returns a dataframe with the same keys, but whose values are taken
		only from the specified line of output.
	- 	``str`` [case-insensitive] : labels of the lists of quantities stored.

		For MDF objects, the following are assigned automatically by VICE when
		reading in the output and will not be re-assigned:

			- 	'bin_edge_left' : Lower bin edges of the distribution
			- 	'bin_edge_right' : Upper bin edges of the distribution
			- 	'dn/d[x/h]' : The value of the probability distribution
				function of stars in their [X/H] logarithmic abundance.
			-	'dn/d[x/y]' : The value of the probability distribution
				function of stars in their [X/Y] logarithmic abundance ratio.

	Functions
	---------
	- keys
	- todict
	- filter

	Example Code
	------------
	>>> import vice
	>>> example = vice.mdf("example")
	>>> example.keys()
		['bin_edge_left',
		 'bin_edge_right',
		 'dn/d[fe/h]',
		 'dn/d[sr/h]',
		 'dn/d[o/h]',
		 'dn/d[sr/fe]',
		 'dn/d[o/fe]',
		 'dn/d[o/sr]']
	>>> example["bin_edge_left"][:10]
		[-3.0, -2.95, -2.9, -2.85, -2.8, -2.75, -2.7, -2.65, -2.6, -2.55]
	>>> example[60]
		vice.dataframe{
			bin_edge_left --> 0.0
			bin_edge_right -> 0.05
			dn/d[fe/h] -----> 0.0
			dn/d[sr/h] -----> 0.0
			dn/d[o/h] ------> 0.0
			dn/d[sr/fe] ----> 0.06001488
			dn/d[o/fe] -----> 0.4337209
			dn/d[o/sr] -----> 0.0
		}

	**Signature**: vice.core.dataframe.fromfile(filename = None,
	labels = None, adopted_solar_z = None)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe. Fromfile objects are created by various
		functions which read in simulation output (e.g. vice.mdf).

	Parameters
	----------
	filename : ``str`` [default : None]
		The name of the ascii file containing the output.
	list : ``list`` of strings [default : None]
		The strings to assign the column labels.
	adopted_solar_z : real number [default : None]
		The metallicity by mass of the sun :math:`Z_\odot` adopted in the
		simulation.
	"""
	# cdef FROMFILE *_ff

	# Extra keyword arg adopted_solar_z included to not break history object
	def __cinit__(self, filename = None, labels = None,
		adopted_solar_z = None):
		self._ff = _fromfile.fromfile_initialize()

	def __init__(self, filename = None, labels = None,
		adopted_solar_z = None):
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
				if _fromfile.fromfile_modify_column(self._ff, copy,
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

	@property
	def name(self):
		r"""
		Type : ``str``

		The name of the file that this data was read from.

		Example Code
		------------
		>>> import vice
		>>> example = vice.mdf("example")
		>>> example.name
			'example.vice/mdf.out'
		"""
		return "".join([chr(self._ff[0].name[i]) for i in range(
			strlen(self._ff[0].name))])

	@property
	def size(self):
		r"""
		Type : ``tuple``

		Contains two integers: the (length, width) of the dataframe.

		Example Code
		------------
		>>> import vice
		>>> example = vice.mdf("example")
		>>> example.size
			(80, 8)
		"""
		return tuple([self._ff[0].n_rows, self._ff[0].n_cols])
		
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
		labels = self._ff[0].n_cols * [None]
		for i in range(self._ff[0].n_cols):
			labels[i] = "".join([chr(self._ff[0].labels[i][j]) for j in range(
				strlen(self._ff[0].labels[i]))])
		return labels

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
		return dict(zip(self.keys(),
			[self.__getitem__(i) for i in self.keys()]))


	def remove(self, key):
		"""
		This function throws a TypeError whenever called. This derived class
		of the VICE dataframe does not support item deletion.
		"""
		# data is stored in C -> no keys to delete from
		raise TypeError("This dataframe does not support item deletion.")

