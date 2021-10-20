# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..._globals import _DEFAULT_STELLAR_MIGRATION_
from .. import _pyutils
import numbers
from ..objects cimport _migration
from . cimport _migration
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError


cdef class mig_specs:

	r"""
	Multizone simulation migration prescriptions for gas and stars.

	**Signature**: vice.migration.specs(n)

	.. versionadded:: 1.2.0

	Parameters
	----------
	n : ``int``
		The number of rows and columns in the gas migration matrix. This is
		also the number of zones in a multizone model.

	Attributes
	----------
	gas : ``mig_matrix``
		A matrix containing the mass fraction of gas moving between zones.
	stars : <function>
		A function of the zone number and time of star formation. Expected to
		return a function of time in Gyr describing the zone number at all
		subsequent times of stars forming in that zone at that time.

	Example Code
	------------
	>>> import math
	>>> import vice
	>>> example = vice.migration.specs(3)
	>>> def f(zone, tform, time):
		# swap stars between zones 0 and 1 when they're >1 Gyr old.
		if zone == 0:
			if time - tform > 1:
				return 1
			else:
				return 0
		elif zone == 1:
			if time - tform > 1:
				return 0
			else:
				return 1
		else:
			return zone
	>>> example.stars = f
	>>> example.gas[1][0] = 0.1
	>>> def g(t):
		return 0.2 * math.exp(-t / 2)
	>>> example.gas[0][1] = g
	>>> example.gas
		MigrationMatrix{
			0 ---------> {0.0, <function g at 0x120588560>, 0.0}
			1 ---------> {0.1, 0.0, 0.0}
			2 ---------> {0.0, 0.0, 0.0}
		}
	"""

	def __init__(self, n):
		# type checking in multizone object
		assert isinstance(n, int), "Must be of type int. Got: %s" % (type(n))
		self.stars = _DEFAULT_STELLAR_MIGRATION_
		self._gas = mig_matrix(n)

	def __repr__(self):
		rep = "Stars: %s\n" % (str(self._stars))
		for i in range(22):
			rep += ' '
		rep += "Gas: "
		for i in str(self._gas).split('\n'):
			rep += "    %s\n" % (i)
		return rep

	def __str__(self):
		return self.__repr__()

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

	@property
	def gas(self):
		r"""
		Type : ``migration_matrix``

		Default: Zeroes (i.e. no gas migration)

		The gas migration matrix. For a multizone simulation with N zones,
		this is an NxN matrix.

		This matrix is defined such that :math:`G_{ij}` represents the
		mass fraction of gas that moves from the :math:`i`'th zone to the
		:math:`j`'th zone in a 10 Myr time interval.

		Allowed Types
		-------------
		* 	real number
			The fraction of gas that migrates in a 10 Myr time interval is
			constant, given by this value.
		* 	<function>
			Must accept time in Gyr as the only parameter. The fraction of gas
			that migrates in a 10 Myr time interval varies with time, and is
			described by this function.

		Notes
		-----
		The mass fraction of interstellar gas that migration from zone
		:math:`i` to zone :math:`j` at a time :math:`t` is calculated via

		.. math:: f_{ij}(t) = G_{ij}(t) \frac{\Delta t}{\text{10 Myr}}

		The mass that migrates is then given by :math:`M_{g,i} f_{ij}(t)`,
		where :math:`M_{g,i}` is the total mass of the interstellar medium in
		zone :math:`i`.

		This guarantees that the amount of gas that migrates in a given time
		interval does not depend on the timestep size.

		Example Code
		------------
		>>> import math
		>>> import vice
		>>> example = vice.migration.specs(3)
		>>> example.gas[1][0] = 0.1
		>>> def f(t):
			return math.exp(-t / 2)
		>>> example.gas[0][1] = f
		>>> example.gas
			MigrationMatrix{
				0 ---------> {0.0, <function f at 0x120588560>, 0.0}
				1 ---------> {0.1, 0.0, 0.0}
				2 ---------> {0.0, 0.0, 0.0}
			}
		"""
		return self._gas

	@gas.setter
	def gas(self, value):
		if isinstance(value, mig_matrix):
			if value.size == self._gas.size:
				self._gas = value
			else:
				raise ValueError("""Migration matrix of incorrect size. \
Got: %d. Required: %d.""" % (value.size, self._gas.size))
		else:
			raise TypeError("""Attribute 'gas' must be of type \
'migration_matrix'. Got: %s""" % (type(value)))

	@property
	def stars(self):
		r"""
		Type : <function>

		Default : vice._globals._DEFAULT_STELLAR_MIGRATION_

		.. note:: The default migration setting does not move stars between
			zones at all.

		The stellar migration prescription.

		This function must accept at ``int`` followed by two real numbers as
		parameters, in that order. These are interpreted as the zone number in
		which a star particle forms in a multizone simulation, the time at
		which it forms in Gyr, and the time in the simulation in Gyr.

		This function must return an ``int`` describing the zone number of the
		star particle at times following its formation.

		Notes
		-----
		The third parameter returned by this function is interpreted as the
		time since the start of the simulation, **NOT** the age of the star
		particle in question.

		This function will never be called with a third parameter that is
		smaller than the second parameter. These are times at which star
		particles have not formed yet.

		.. tip:: If users wish to write extra data for star particles to an
			output file, they should set up this attribute as an instance of
			a class. If this class has an attribute ``write``, VICE will switch
			it's value to ``True`` when setting up star particles for
			simulation. The lines which write to the output file can then be
			wrapped in an ``if self.write`` statement.

		.. tip:: If a multizone simulation will form multiple star particles
			per zone per timestep, they can be assigned different zone
			occupation histories by allowing the function of initial zone
			number and formation time to take a keyword argument ``n``.
			VICE will then call this function with ``n = 0``, ``n = 1``,
			``n = 2``, and so on up to ``n = n_stars - 1``, where ``n_stars``
			is the number of star particles per zone per timestep.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.specs(3)
		>>> def f(zone, tform, time):
			# swap stars between zones 0 and 1 when they're >1 Gyr old
			if zone == 0:
				if time - tform > 1:
					return 1
				else:
					return 0
			elif zone == 1:
				if time - tform > 1:
					return 0
				else:
					return 1
			else:
				return zone
		>>> example.stars = f
		"""
		return self._stars

	@stars.setter
	def stars(self, value):
		if callable(value):
			if _pyutils.arg_count(value) == 3:
				self._stars = value
			else:
				raise TypeError("""Stellar migration setting must accept \
three numerical parameters.""")
		else:
			raise TypeError("""Stellar migration setting must be a callable \
object.""")


cdef class mig_matrix:

	r"""
	A square matrix designed to detail the manner in which gas migrates
	between zones in multizone models. This is a 2-dimensional array-like
	object denoted by :math:`G_{ij}`, defined as the mass fraction of the
	interstellar gas in zone :math:`i` that migrates to zone :math:`j` in a
	10 Myr time interval.

	**Signature**: vice.migration.migration_matrix(size)

	.. versionadded:: 1.2.0

	Parameters
	----------
	size : ``int``
		The number of rows and columns. This is also the number of zones in
		the multizone model.

	Attributes
	----------
	size : ``int``
		See parameter "size".

	Allowed Data Types
	------------------
	* real number
		:math:`G_{ij}` does not vary with time, and is given by this value.
	* <function>
		:math:`G_{ij}` varies with time, and is described by this function.
		Time in Gyr is the only parameter the function takes.

	Indexing
	--------
	- ``int``, ``int`` : the row and column numbers
		The value of :math:`G_{ij}` can be accessed by indexing this object
		with :math:`i` as the first index and :math:`j` as the second. For
		instance, ``example[1][0]`` and ``example[1, 0]`` both look up
		:math:`G_{1,0}`.

	Functions
	---------
	- tolist
	- tonumpyarray

	Example Code
	------------
	>>> import math
	>>> import vice
	>>> example = vice.migration.migration_matrix(3)
	>>> example
		MigrationMatrix{
			0 ---------> {0.0, 0.0, 0.0}
			1 ---------> {0.0, 0.0, 0.0}
			2 ---------> {0.0, 0.0, 0.0}
		}
	>>> example[1][0] = 0.1
	>>> def f(t):
		return 0.1 * math.exp(-t / 5)
	>>> example[0, 1] = f
	>>> example
		MigrationMatrix{
			0 ---------> {0.0, <function f at 0x120588560>, 0.0}
			1 ---------> {0.1, 0.0, 0.0}
			2 ---------> {0.0, 0.0, 0.0}
		}
	>>> example.tonumpyarray()
		array([[0.0, <function f at 0x120588560>, 0.0],
			[0.0, 0.0, 0.0],
			[0.0, 0.0, 0.0]])
	"""

	def __init__(self, size):
		# multizone object will perform this type-checking
		assert isinstance(size, int), "Must be an integer number of zones."
		assert size > 0, "Negative number of zones"

		self._rows = size * [None]
		for i in range(size):
			self._rows[i] = mig_matrix_row(size)

	def __getitem__(self, key):
		if isinstance(key, tuple):
			if len(key) > 2:
				raise IndexError("Too many indeces: %s" % (key))
			else:
				key1 = key_check(key[0], self.size)
				key2 = key_check(key[1], self.size)
				if isinstance(key1, list):
					# error to raise, replace type w/IndexError
					raise IndexError(key1[1])
				elif isinstance(key2, list):
					# error to raise replace type w/IndexError
					raise IndexError(key2[1])
				else:
					return self._rows[key1][key2]
		else:
			key = key_check(key, self.size)
			if isinstance(key, int):
				# user passed the proper type
				return self._rows[key]
			elif isinstance(key, list):
				# exception to raise, replace type w/IndexError
				raise IndexError(key[1])
			else:
				# shouldn't happen
				raise SystemError("Internal Error")

	def __setitem__(self, key, value):
		if isinstance(key, tuple):
			if len(key) > 2:
				raise IndexError("Too many indeces: %s" % (str(key)))
			else:
				key1 = key_check(key[0], self.size)
				key2 = key_check(key[1], self.size)
				if isinstance(key1, list):
					# exception to raise
					raise key1[0](key1[1])
				elif isinstance(key2, list):
					# exception to raise
					raise key2[0](key2[1])
				else:
					# row.__setitem__ handles further exceptions
					self._rows[key1][key2] = value
		elif isinstance(key, numbers.Number) and key % 1:
			raise TypeError("""Assignment of entire row of migration matrix \
not supported. Please modify each element individually.""")
		else:
			raise TypeError("""Item assignment requires two keys of type int.
Got: %s""" % (type(key)))

	def __repr__(self):
		rep = "MigrationMatrix{\n"
		for i in range(self.size):
			rep += "    %d " % (i)
			for j in range(10 - len(str(i))):
				rep += '-'
			rep += "> %s\n" % (str(self._rows[i]))
		rep += "}"
		return rep

	def __str__(self):
		return self.__repr__()

	@property
	def size(self):
		r"""
		Type : ``int`` [positive definite]

		The number of rows and columns of this matrix. This is also the number
		of zones in the multizone model.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.migration_matrix(3)
		>>> example.size
			3
		"""
		return self._rows[0].size

	def tolist(self):
		r"""
		Obtain a copy of this migration matrix as a list.

		**Signature**: x.tolist()

		Parameters
		----------
		x : ``migration_matrix``
			An instance of this class.

		Returns
		-------
		copy : ``list``
			A list of all values in this matrix.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.migration_matrix(3)
		>>> example.tolist()
			[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		"""
		return [i.tolist() for i in self._rows]

	def tonumpyarray(self):
		r"""
		Obtain a copy of this migration matrix as a `NumPy`__ array.

		**Signature**: x.tonumpyarray()

		Parameters
		----------
		x : ``migration_matrix``
			An instance of this class.

		Returns
		-------
		copy : numpy.ndarray
			A `NumPy`__ array which stores the same values as ``x``.

		Raises
		------
		* ModuleNotFoundError [ImportError for python < 3.6]
			- `NumPy`__ could not be imported.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.migration_matrix(3)
		>>> example.tonumpyarray()
			array([[0, 0, 0],
				[0, 0, 0],
				[0, 0, 0]])

		__ numpy_
		__ numpy_
		__ numpy_
		.. _numpy: https://numpy.org
		"""
		try:
			import numpy as np
		except (ModuleNotFoundError, ImportError):
			raise ModuleNotFoundError("NumPy not found.")
		return np.array(self.tolist())


cdef class mig_matrix_row:

	r"""
	A row of a migration matrix. This is a 1-dimension arary-like object
	whose elements denote the mass fraction of interstellar gas that migrates
	out of one zone and into other zones in a 10 Myr time interval in a
	multizone simulation.

	.. seealso:: vice.migration.migration_matrix

	.. note:: Creation of new instances of this class is discouraged. This
		object only has use in the ``migration_matrix`` object, and it is
		recommended that users let that class generate instances of this
		class automatically.

	.. versionadded:: 1.2.0

	Attributes
	----------
	size : ``int``
		The number of elements stored by this array-like object.

	Allowed Data Types
	------------------
	- real number
		The amount of gas migrating out of this zone and into another does
		not vary with time, and is given by this value.
	- <function>
		The amount of gas migrating out of this zone and into another varies
		with time, and is described by this function.

	Indexing
	--------
	- ``int``
		The element of this array to access.

	Functions
	---------
	- tolist
	- tonumpyarray

	Example Code
	------------
	>>> import vice
	>>> example = vice.migration.migration_matrix(3)
	>>> example[0].size
		3
	>>> example[0].tolist()
		[0, 0, 0]
	>>> example[0].tonumpyarray()
		array([0, 0, 0])
	"""

	def __init__(self, size):
		self.size = size # type checking in setter routine
		self._row = self.size * [0.]

	def __getitem__(self, key):
		key = key_check(key, self.size)
		if isinstance(key, int):
			# user passed the proper type
			return self._row[key]
		elif isinstance(key, list):
			# exception to raise, replace type w/IndexError
			raise IndexError(key[1])
		else:
			# shouldn't happen
			raise SystemError("Internal Error")

	def __setitem__(self, key, value):
		key = key_check(key, self.size)
		if isinstance(key, numbers.Number) and key % 1 == 0:
			key = int(key)
			# user passed the proper type
			if isinstance(value, numbers.Number):
				"""
				Don't enforce probability to be less than 1. The probabilities
				are normalized to a 10 Myr interval, and that can only be
				taken into account upon runtime.
				"""
				self._row[key] = float(value)
			elif callable(value):
				_pyutils.args(value, """Functional element of migration \
matrix must accept only one numerical parameter.""")
				self._row[key] = value
			else:
				raise TypeError("""Migration matrix element must be either a \
real number or a callable function. Got: %s""" % (type(value)))
		elif isinstance(key, list):
			# exception to raise
			raise key[0](key[1])
		else:
			# shouldn't happen
			raise SystemError("Internal Error")

	def __repr__(self):
		# return "{%s}" % (str(self._row))
		return str(self._row).replace('[', '{').replace(']', '}')

	def __str__(self):
		return self.__repr__()

	@property
	def size(self):
		r"""
		Type : ``int`` [positive definite]

		The number of elements stored by this array-like object.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.migration_matrix(3)
		>>> example[0].size
			3
		"""
		return self._size

	@size.setter
	def size(self, value):
		if isinstance(value, numbers.Number):
			if value > 0:
				if value % 1 == 0:
					self._size = int(value)
				else:
					raise ValueError("""Attribute 'size' must be \
interpretable as an integer. Got: %g""" % (value))
			else:
				raise ValueError("Attribute 'size' must be positive.")
		else:
			raise TypeError("""Attribute 'size' must be an integer. \
Got: %s""" % (type(value)))

	def tolist(self):
		r"""
		Obtain a copy of this object as a list.

		**Signature**: x.tolist()

		Parameters
		----------
		x : ``mig_matrix_row``
			An instance of this class.

		Returns
		-------
		copy : ``list``
			A list comprehension of all values in this array.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.migration_matrix(3)
		>>> example[0].tolist()
			[0, 0, 0]
		"""
		return self._row

	def tonumpyarray(self):
		r"""
		Obtain a copy of this array-like object as a `NumPy`__ matrix.

		**Signature**: x.tonumpyarray()

		Parameters
		----------
		x : ``mig_matrix_row``
			An instance of this class.

		Returns
		-------
		copy : numpy.ndarray
			A `NumPy`__ array which stores the same values as ``x``.

		Raises
		------
		* ModuleNotFoundError [ImportError for python < 3.6]
			- `NumPy`__ could not be imported.

		Example Code
		------------
		>>> import vice
		>>> example = vice.migration.migration_matrix(3)
		>>> example[0].tonumpyarray()
			array([0, 0, 0])

		__ numpy_
		__ numpy_
		__ numpy_
		.. _numpy: https://numpy.org
		"""
		try:
			import numpy as np
		except (ModuleNotFoundError, ImportError):
			raise ModuleNotFoundError("NumPy not found.")
		return np.array(self.tolist())


def key_check(key, maximum):
	"""
	Performs exception-handling checks to ensure that key is an integer
	between 0 and maximum - 1 (inclusive)

	Parameters
	==========
	key :: object
		The value to type and value check
	maximum :: int
		The length of an array

	Returns
	=======
	If key is allowed:
		key :: int
			The key itself
	Else:
		exc :: Exception
			The exception type to raise
		msg :: str
			The message to raise with the exception
	"""
	if isinstance(key, numbers.Number):
		if 0 <= key < maximum:
			if key % 1 == 0:
				return int(key)
			else:
				return [ValueError,
					"Index must be interpretable as an integer. Got: %g" % (
					key)]
		else:
			return [ValueError, "Index out of bounds: %g" % (key)]
	else:
		return [TypeError, "Index must be an integer. Got: %s" % (type(key))]

