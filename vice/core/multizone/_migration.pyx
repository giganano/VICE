# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..._globals import _DEFAULT_STELLAR_MIGRATION_ 
from .. import _pyutils 
import numbers 
from ..objects cimport _migration 
from . cimport _migration 


cdef class mig_specs: 

	r""" 
	Multizone simulation migration prescriptions for gas and stars. 

	**Signature**: vice.migration.specs(n) 

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
	>>> def f(zone, tform): 
		def g(time): 
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
		return g 
	>>> example.stars = f 
	>>> example.gas[1][0] = 0.1 
	>>> def h(t): 
		return 0.2 * math.exp(-t / 2) 
	>>> example.gas[0][1] = h 
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
		rep += "ISM: " 
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

		.. math:: f_{ij} = G_{ij}(t) \frac{\Delta t}{\text{10 Myr}} 

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

		This function must accept an ``int`` and a real number as the first 
		and second parameters, respectively. These are interpreted as the zone 
		number and time at which a star particle forms in a multizone 
		simulation. 

		This attribute must return another function, which must accept a real 
		number as the only parameter. This is interpreted as time in Gyr. This 
		is **NOT** the *age* of the star particle, but rather the time since 
		the start of a multizone simulation (the same interpretation as the 
		formation time of the star particle). This function must then return 
		an ``int`` describing the zone number of the star particle at times 
		following its formation. 

		.. tip:: If users wish to write extra data for star particles to an 
			output file, they should set up this attribute as an instance of 
			a class (see the final tip below). If this class has an attribute 
			``write``, VICE will switch it's value to ``True`` when setting 
			up star particles for simulation. The lines which write to the 
			output file can then be wrapped in an ``if self.write:`` 
			statement. 

		.. tip:: If a multizone simulation will form multiple star particles 
			per zone per timestep, they can be assigned different zone 
			occupation histories by allowing the function of initial zone 
			number and formation time to take a keyword argument ``n``. 
			VICE will then call this function with ``n = 1``, ``n = 2``, 
			``n = 3``, and so on up to ``n = n_stars``, where ``n_stars`` 
			is the number of star particles per zone per timestep. 

		.. tip:: These functions need not be produced via ``def`` statements. 
			They may also be instances of classes with a ``__call__`` 
			function. An example of such a technique can be found in VICE's 
			`git repository`__. 

			__ git_repo_ 
			.. _git_repo: https://github.com/giganano/VICE.git 

		Example Code 
		------------
		>>> import vice 
		>>> example = vice.migration.specs(3) 
		>>> def f(zone, tform): 
			def g(time): 
				# stars forming in zones 0 and 1 swap when >1 Gyr old 
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
					# else no migration 
					return zone 
			return g 
		>>> example.stars = f 
		""" 
		return self._stars 

	@stars.setter 
	def stars(self, value): 
		if callable(value): 
			try: 
				x = value(0, 0) 
			except TypeError: 
				raise ValueError("""Stellar migration setting must accept \
two numerical parameters.""") 
			if callable(x): 
				try: 
					x(0) 
				except TypeError: 
					raise ValueError("""Stellar migration setting must return \
an object accepting one numerical parameter.""") 
				self._stars = value 
			else: 
				raise TypeError("""Stellar migration setting must return a \
callable object.""") 
		else: 
			raise TypeError("""Stellar migration setting must be a callable \
object.""") 


cdef class mig_matrix: 

	""" 
	Contains user-specified migration prescriptions for use in multizone 
	simulations. For a multizone simulation with N zones, this is an NxN 
	matrix. 

	This matrix is defined such that the ij'th element represents the 
	likelihood that interstellar gas will migrate FROM the i'th TO the j'th 
	zone in the simulation within a 10 Myr time interval. 

	Unallowed numerical values will not raise exceptions here, but will upon 
	running a multizone object. 

	Attributes 
	========== 
	size :: int 
		The number of zones in the migration matrix 
	""" 

	def __init__(self, size): 
		""" 
		Args 
		==== 
		size :: int 
			The number of zones in the migration matrix 
		""" 
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
		else: 
			raise TypeError("""Assignment of entire row of migration matrix \
not supported. Please modify each element individually.""")  

	def __repr__(self): 
		rep = "MigrationMatrix{\n" 
		for i in range(self.size): 
			rep += "    Zone %d %s\n" % (i, str(self._rows[i])) 
		rep += "}" 
		return rep 

	def __str__(self): 
		return self.__repr__() 

	@property 
	def size(self): 
		""" 
		Type :: int 

		The number of zones in the simulation. 
		""" 
		return self._rows[0].dimension 

	def tolist(self): 
		""" 
		Obtain a copy of the migration matrix as a list 
		""" 
		return [i.tolist() for i in self._row] 


cdef class mig_matrix_row: 

	""" 
	A row of the migration matrix. For a multizone simulation with N zones, 
	this is an N-element list. 

	This row is defined such that the i'th element represents the likelihood 
	that interstellar gas or stars will migrate FROM this zone TO the i'th 
	zone in the simulation. These entries may be either numerical value or 
	functions of time in Gyr. In all cases, the value at a given time must be 
	between 0 and 1, because the elements are interpreted as likelihoods. 

	Attributes 
	========== 
	dimension :: int 
		The number of zones in the row 
	""" 
	def __init__(self, dimension): 
		""" 
		Args 
		==== 
		dimension :: int 
			The number of zones in the multizone simulation (i.e. length of 
			this array). 
		""" 
		self.dimension = dimension # type checking in setter routine 
		self._row = self.dimension * [0.] 

	def __getitem__(self, key): 
		key = key_check(key, self.dimension) 
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
		key = key_check(key, self.dimension) 
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
		return "Likelihood{%s}" % (str(self._row)) 

	def __str__(self): 
		return self.__repr__() 

	@property 
	def dimension(self): 
		""" 
		Type :: int [positive definite] 

		The number of zones in the simulation. 
		""" 
		return self._dimension 

	@dimension.setter 
	def dimension(self, value): 
		if isinstance(value, numbers.Number): 
			if value > 0: 
				if value % 1 == 0: 
					self._dimension = int(value) 
				else: 
					raise ValueError("""Attribute 'dimension' must be \
interpretable as an integer. Got: %g""" % (value)) 
			else: 
				raise ValueError("Attribute 'dimension' must be positive.") 
		else: 
			raise TypeError("""Attribute 'dimension' must be an integer. \
Got: %s""" % (type(value))) 

	def tolist(self): 
		""" 
		Obtain this row of the migration matrix as a list 
		""" 
		return self._row 



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

