# cython: language_level = 3, boundscheck = False
"""
This file implements the history object, a subclass of the fromfile object.
This class is designed to read in and make calculations with the history.out
file associated with outputs of the singlezone class.
"""

from ..._globals import _VERSION_ERROR_
from ..outputs import _output_utils
from .. import _pyutils
from . import _base
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from libc.stdlib cimport malloc, free
from .._cutils cimport set_string
from . cimport _history


#----------------------------- HISTORY SUBCLASS -----------------------------#
cdef class history(fromfile):

	r"""
	The VICE dataframe: derived class (inherits from fromfile)

	Provides a means of storing and accessing the time-evolution of the
	interstellar medium from the output of a singlezone object. History
	objects can be created from VICE outputs by calling vice.history.

	Attributes
	----------
	name : ``str``
		The name of the file that the data was pulled from.
	size : ``tuple``
		Contains two integers: the (length, width) of the data.

	Allowed Data Types
	------------------
	* Keys
		- ``str`` [case-insensitive] : the physical quantity.
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

			- 	'time' : Time in Gyr from the start of the simulation.
			- 	'lookback' : Lookback time in Gyr from the end of the
				simulation.
			- 	'mgas' : The mass of the interstellar medium in :math:`M_\odot`
			- 	'sfr' : Star formation rate in :math:`M_\odot \text{yr}^{-1}`
			- 	'ifr' : Infall rate in :math:`M_\odot \text{yr}^{-1}`
			- 	'ofr' : Outflow rate in :math:`M_\odot \text{yr}^{-1}`
			- 	'eta_0' : The user-specified value of the mass-loading
				parameter :math:`\eta`, independent of the smoothing timescale
				:math:`\tau_\star` employed in the simulation.
			- 	'r_eff' :	The effective recycling parameter
				:math:`\dot{M}_\text{r}/\dot{M}_\star`.
			- 	'z_in(x)' : The inflow metallicity by mass :math:`Z` of the
				element :math:`x`.
			- 	'z_out(x)' : The outflow metallicity by mass :math:`Z` of the
				element :math:`x`.
			- 	'mass(x)' : The mass of the element :math:`x` in the
				interstellar medium.
			- 	'z(x)' : The metallicity by mass :math:`Z` of the element
				:math:`x` in the interstellar medium.
			- 	'[x/h]' : The logarithmic abundance relative to the sun of the
				element :math:`x`, given by :math:`\log_{10}(Z_x/Z_{x,\odot})`.
			- 	'[y/x]' : The logarithmic abundance ratio relative to the sun
				between the elements :math:`y` and :math:`x`, given by
				:math:`\log_{10}(Z_y/Z_{y,\odot}) - \log_{10}(Z_x/Z_{x,\odot})`.
			- 	'z' : The scaled total metallicity by mass :math:`Z`.
			- 	'[m/h]' : The scalled logarithmic metallicity relative to the
				sun, given by :math:`\log_{10}(Z/Z_\odot)`.

		.. note:: The scaled total metallicity by mass is defined by:

			.. math:: Z = Z_\odot \frac{\sum_i Z_i}{\sum_i Z_{i,\odot}}

			where :math:`Z_\odot` is the metallicity of the sun adopted in the
			simulation, and :math:`Z_i` is the abundance by mass of the i'th
			element. This scaling is employed so that an accurate estimation
			of the total metallicity can be obtained without every element's
			abundance information.

		.. note:: The scaled logarithmic metallicity is defined from the
			scaled total metallcity by mass according to:

			.. math:: [M/H] = \log_{10}\left(\frac{Z}{Z_\odot}\right)

	Functions
	---------
	- keys
	- todict
	- filter

	Example Code
	------------
	>>> example = vice.history("example")
	>>> example.keys()
		['time',
		 'mgas',
		 'mstar',
		 'sfr',
		 'ifr',
		 'ofr',
		 'eta_0',
		 'r_eff',
		 'z_in(fe)',
		 'z_in(sr)',
		 'z_in(o)',
		 'z_out(fe)',
		 'z_out(sr)',
		 'z_out(o)',
		 'mass(fe)',
		 'mass(sr)',
		 'mass(o)',
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
		 'lookback']
	>>> example[100]
		vice.dataframe{
			time -----------> 1.0
			mgas -----------> 5795119000.0
			mstar ----------> 2001106000.0
			sfr ------------> 2.897559
			ifr ------------> 9.1
			ofr ------------> 7.243899
			eta_0 ----------> 2.5
			r_eff ----------> 0.3534769
			z_in(fe) -------> 0.0
			z_in(sr) -------> 0.0
			z_in(o) --------> 0.0
			z_out(fe) ------> 0.0002769056
			z_out(sr) ------> 3.700754e-09
			z_out(o) -------> 0.001404602
			mass(fe) -------> 1604701.0
			mass(sr) -------> 21.44631
			mass(o) --------> 8139837.0
			z(fe) ----------> 0.0002769056166059748
			z(sr) ----------> 3.700754031107903e-09
			z(o) -----------> 0.0014046022178319376
			[fe/h] ---------> -0.6682579454664828
			[sr/h] ---------> -1.1074881208001155
			[o/h] ----------> -0.6098426789720387
			[sr/fe] --------> -0.43923017533363273
			[o/fe] ---------> 0.05841526649444406
			[o/sr] ---------> 0.4976454418280768
			z --------------> 0.0033582028978416337
			[m/h] ----------> -0.6200211036287412
			lookback -------> 9.0
		}

	**Signature**: vice.core.dataframe.history(filename = None,
	adopted_solar_z = None, labels = None)

	.. warning:: Users should avoid creating new instances of derived classes
		of the VICE dataframe. To obtain a history object from a VICE output,
		simply call vice.history.

	Parameters
	----------
	filename : ``str`` [default : None]
		The name of the ascii file containing the history output.
	adopted_solar_z : real number [default : None]
		The metallicity by mass of the sun :math:`Z_\odot` adopted in the
		simulation.
	labels : ``list`` of strings [default : None]
		The strings to assign the column labels.
	"""

	# cdef char **_elements
	# cdef unsigned int n_elements
	# cdef double *solar
	# cdef double Z_solar

	def __init__(self, filename = None, labels = None,
		adopted_solar_z = None):
		super().__init__(filename = filename, labels =
			_output_utils._load_column_labels_from_file_header(filename))
		elements = self._load_elements()
		self._n_elements = <unsigned> len(elements)
		self._elements = <char **> malloc (self._n_elements * sizeof(char *))
		for i in range(self._n_elements):
			self._elements[i] = <char *> malloc ((len(elements) + 1) *
				sizeof(char))
			set_string(self._elements[i], elements[i])
		self._solar = <double *> malloc (self._n_elements * sizeof(double))
		from ._builtin_dataframes import solar_z
		for i in range(self._n_elements):
			self._solar[i] = solar_z[elements[i]]
		self._Z_solar = adopted_solar_z

	def _load_elements(self):
		elements = []
		for i in _output_utils._load_column_labels_from_file_header(self.name):
			if i.startswith("mass("):
				# Find elements based on the columns of reported masses
				elements.append("%s" % (i.split('(')[1][:-1].lower()))
			else:
				continue
		return tuple(elements[:])

	def __getitem__(self, key):
		"""
		Can be indexed via both str and int, allow negative indexing as well.
		Special strings [m/h] and z recognized for automatic calculation of
		scaled total ISM metallicity.
		"""
		if isinstance(key, strcomp):
			return self.__subget__str(key)
		elif isinstance(key, numbers.Number) and key % 1 == 0:
			return self.__subget__int(key)
		else:
			# No error yet, other possibilities in super's __getitem__
			return super().__getitem__(key)

	def __subget__str(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str
		"""
		# See docstrings of subroutines for further info
		if key.lower().startswith("z(") and key.endswith(')'):
			return self.__subget__str_z(key)
		elif key.lower() == "y":
			return self.__subget__str_y(key)
		elif key.lower() == "z":
			return self.__subget__str_ztot(key)
		elif key.lower() == "[m/h]":
			return self.__subget__str_logztot(key)
		elif key.startswith('[') and key.endswith(']') and '/' in key:
			return self.__subget__str_logzratio(key)
		elif key.lower() == "lookback":
			return self.__subget__str_lookback(key)
		else:
			# No error yet, other possibilities in super's __getitem__
			return super().__subget__str(key)

	def __subget__str_z(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting a metallicity by mass Z of a given element.
		"""
		cdef double *item
		cdef char *copy
		element = key.split('(')[1][:-1].lower()
		copy = <char *> malloc ((len(element) + 1) * sizeof(char))
		set_string(copy, element.lower())
		item = _history.history_Z_element(self._ff, copy)
		free(copy)
		if item is not NULL:
			x = [item[i] for i in range(self._ff[0].n_rows)]
			free(item)
			return x
		else:
			raise KeyError("Element not tracked by simulation: %s" % (
				element))

	def __subget__str_y(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting the helium mass fraction Y.
		"""
		return self.__subget__str_z("z(he)")

	def __subget__str_ztot(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting the total metallicity by mass Z
		"""
		cdef double *item
		item = _history.history_Zscaled(self._ff, self._n_elements,
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
		item = _history.history_logarithmic_scaled(self._ff, self._n_elements,
			self._elements, self._solar)
		if item is not NULL:
			x = [item[i] for i in range(self._ff[0].n_rows)]
			free(item)
			return x
		else:
			raise SystemError("Internal Error")

	def __subget__str_logzratio(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting a logarithmic abundance ratio [X/Y]. This is generalized to
		handle absolute abundances in the case that [X/H] is passed.
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
		item = _history.history_logarithmic_abundance_ratio(self._ff,
			copy, copy2, self._elements, self._n_elements, self._solar)
		free(copy)
		free(copy2)
		if item is not NULL:
			x = [item[i] for i in range(self._ff[0].n_rows)]
			free(item)
			return x
		else:
			raise KeyError("Unrecognized dataframe key: %s" % (key))

	def __subget__str_lookback(self, key):
		"""
		Performs the __getitem__ operation when the key is of type str and is
		requesting the lookback time.
		"""
		assert key.lower() == "lookback", "Internal Error"
		cdef double *item = _history.history_lookback(self._ff)
		if item is not NULL:
			x = [item[i] for i in range(self._ff[0].n_rows)]
			free(item)
			return x
		else:
			raise SystemError("Internal Error")

	def __subget__int(self, key):
		"""
		Performs the __getitem__ operation when the key is of type int.
		"""
		cdef double *item
		if 0 <= key < self._ff[0].n_rows:
			item = _history.history_row(self._ff, <unsigned long> key,
				self._elements, self._n_elements, self._solar, self._Z_solar)
		elif abs(key) <= self._ff[0].n_rows:
			item = _history.history_row(self._ff,
				self._ff[0].n_rows - <unsigned long> abs(key),
				self._elements, self._n_elements, self._solar, self._Z_solar)
		else:
			raise IndexError("Index out of bounds: %d" % (int(key)))
		if item is not NULL:
			x = [item[i] for i in range(_history.history_row_length(self._ff,
				self._n_elements, self._elements))]
			free(item)
			return _base.base(dict(zip(self.keys(), x)))
		else:
			raise SystemError("Internal Error")

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
		keys = super().keys()
		elements = self._load_elements()
		for i in elements:
			keys.append("z(%s)" % (i))
		for i in elements:
			keys.append("[%s/h]" % (i))
		for i in range(1, len(elements)):
			for j in range(i):
				keys.append("[%s/%s]" % (elements[i], elements[j]))
		keys.append("z")
		keys.append("[m/h]")
		keys.append("lookback")
		if "he" in elements: keys.append("y")
		return keys

