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
from . cimport _base


cdef class tracers(history):

	r"""
	The VICE dataframe: derived class (inherits from history)

	Provides a means of storing and accessing the star particles formed in a
	multizone simulation. Tracers objects can be created from VICE outputs
	by calling vice.stars.

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
				output which cannot be overridden. A list of them can be
				found here under `Indexing`_.

	* Values
		- array-like
			Must have the same length as the values of the dataframe obtained
			from the output file.

	Indexing
	--------
	- ``int`` : A given line-number of output.
		Returns a dataframe with the same keys, but whose values are taken
		only from the specified line of output.
	- ``str`` [case-insensitive] : labels of the lists of quantities stored.
		The following are assigned automatically by VICE when reading in an
		output file and will not be re-assigned:

			- 	'formation_time' : Time in Gyr from the start of the
				simulation when a star particle formed.
			- 	'zone_origin' : The zone number the star formed in.
			- 	'zone_final' : The zone number of the star at the end of the
				simulation.
			- 	'mass' : The mass of the star particle in :math:`M_\odot`.
			- 	'z(x)' : The metallicity by mass :math:`Z` of the element
				:math:`x` in that star particle.
			- 	'[x/h]' : The logarithmic abundance relative to the sun of the
				element :math:`x`, given by :math:`\log_{10}(Z_x/Z_{x,\odot})`.
			- 	'[y/x]' : The logarithmic abundance ratio relative to the sun
				between the elements :math:`y` and :math:`x`, given by
				:math:`\log_{10}(Z_y/Z_{y,\odot}) - \log_{10}(Z_x/Z_{x,\odot})`.
			- 	'z' : The scaled toatl metallicity by mass :math:`Z`.
			- 	'[m/h]' : The scaled logarithmic metallicity relative to the
				sun, given by :math:`\log_{10}(Z/Z_\odot)`.

		.. note:: The scaled total metallicity by mass is defined by:

			.. math:: Z = Z_\odot \frac{\sum_i Z_i}{\sum_i Z_{i,\odot}}

			where :math:`Z_\odot` is the metallicity of the sun adopted in the
			simulation, and :math:`Z_i` is the abundance by mass of the i'th
			element. This scaling is employed so that an accurate estimation
			of the total metallicity can be obtained without every element's
			abundance information.

		.. note:: The scaled logarithmic metallicity is defined from the
			scaled total metallicity by mass according to:

			.. math:: [M/H] = \log_{10}\left(\frac{Z}{Z_\odot}\right)

	Functions
	---------
	- keys
	- todict
	- filter

	Example Code
	------------
	>>> example = vice.stars("example")
	>>> example.keys()
		['formation_time',
		 'zone_origin',
		 'zone_final',
		 'mass',
		 'z(fe)',
		 'z(sr)',
		 'z(o)',
		 '[fe/h]',
		 '[sr/h]',
		 '[o/h]',
		 '[sr/fe]',
		 '[o/fe]',
		 '[o/sr]',
		 'z',
		 '[m/h]',
		 'age']
	>>> example[100]
		vice.dataframe{
			formation_time -> 0.1
			zone_origin ----> 0.0
			zone_final -----> 0.0
			mass -----------> 29695920.0
			z(fe) ----------> 1.128362e-05
			z(sr) ----------> 6.203682e-10
			z(o) -----------> 0.0002587532
			[fe/h] ---------> -2.058141258363775
			[sr/h] ---------> -1.8831288138453521
			[o/h] ----------> -1.3445102993763647
			[sr/fe] --------> 0.17501244451842268
			[o/fe] ---------> 0.7136309589874101
			[o/sr] ---------> 0.5386185144689875
			z --------------> 0.0005393007991864363
			[m/h] ----------> -1.4142969718113587
			age ------------> 9.9
		}

	**Signature**: vice.core.dataframe.tracers(filename = None,
	adopted_solar_z = None, labels = None)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe. To obtain a tracers object from a VICE output,
		simply call vice.stars.

	Parameters
	----------
	filename : ``str`` [default : None]
		The name of the ascii file containing the tracers output.
	adopted_solar_z : real number [default : None]
		The metallicity by mass of the sun :math:`Z_\odot` adopted in the
		simulation.
	labels : ``list`` of strings [default : None]
		The strings to assign the column labels.
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
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting the age of the star particles.
		"""
		cdef double *item
		item = _tracers.tracers_age(self._ff)
		if item is not NULL:
			x = [item[i] for i in range(self._ff[0].n_rows)]
			free(item)
			return x
		else:
			raise SystemError("Internal Error")

	def __subget__str_logzratio(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting an abundance ratio [x/Y].
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
				self._n_elements, self._elements))]
			free(item)
			return _base.base(dict(zip(self.keys(), x)))

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
		elements = self._load_elements()
		for i in elements:
			labels.append("[%s/h]" % (i))
		for i in range(1, len(elements)):
			for j in range(i):
				labels.append("[%s/%s]" % (elements[i], elements[j]))
		labels.append("z")
		labels.append("[m/h]")
		labels.append("age")
		if "he" in elements: labels.append("y")
		return labels

