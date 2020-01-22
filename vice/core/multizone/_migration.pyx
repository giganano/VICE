# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..._globals import _DEFAULT_TRACER_MIGRATION_ 
from .. import _pyutils 
import numbers 
from . cimport _migration 


cdef class mig_specs: 

	""" 
	Migration specifications for multizone objects. 

	Attributes 
	========== 
	gas :: mig_matrix 
		A matrix containing mass fractions of migration between zones. 
	stars :: <function> 
		A callable object of initial zone number and time, expected to return 
		a callable function of time, detailing tracer particle zones of 
		occupation. 
	""" 

	def __init__(self, n): 
		""" 
		Args 
		==== 
		n :: int 
			The number of zones in the migration matrix. 
		""" 
		# type checking in multizone object 
		assert isinstance(n, int), "Must be of type int. Got: %s" % (type(n)) 
		self.stars = _DEFAULT_TRACER_MIGRATION_ 
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
		""" 
		The migration matrix associated with the interstellar gas. 

		Contains user-specified migration prescriptions for use in multizone 
		simulations. For a multizone simulation with N zones, this is an NxN 
		matrix. 

		This matrix is defined such that the ij'th element represents the 
		likelihood that interstellar gas or stars will migrate FROM the i'th 
		TO the j'th zone in the simulation during a 10 Myr time interval. 
		These entries may be either numerical values or functions of time in 
		Gyr. In all cases, the value at a given time must be between 0 and 1, 
		because the elements are interpreted as likelihoods. 
		""" 
		return self._gas 

	@property 
	def stars(self): 
		""" 
		The migration settings associated with the stellar tracer particles. 

		This must be a callable object accepting two numerical parameters and 
		optionally a keyword argument "n". The first parameter will be 
		interpreted as the initial zone number of a tracer particle, and the 
		second its formation time in Gyr. If a keyword argument "n" is accepted, 
		it is interpreted as the index of the tracer particle that forms in 
		that zone at that time. Upon setting up the user's multizone simulation, 
		VICE will then call this function with "n" = 0, "n" = 1, "n" = 2, ... , 
		"n" = n_tracers - 1. That is, if the user wishes to treat multiple 
		tracer particles forming in the same zone at the same time differently, 
		they must do so via a keyword argument "n" to this callable object. 

		The returned value from this function must itself also be a callable 
		object, accepting only one numerical parameter and returning an 
		integer. The accepted parameter is interpreted as the zone occupation 
		number as a function of time in Gyr, and the returned value as the 
		zone number of that tracer particle at that time. 

		In this manner, users may manipulate the detailed zone occupation of 
		every individual tracer particle in their simulation as a function of 
		time. 

		Notes 
		===== 
		The function of time describing the zone number of each tracer particle 
		is interpreted as the time in the simulation, not the age of the 
		tracer particle. Times in the simulation before a given tracer particle 
		forms are neglected. 

		The function of time describing an individual tracer particle's zone 
		occupation evaluated at its formation time must match the zone from 
		which the tracer particle forms. If this is ever not the case, an 
		exception will be raised when a multizone simulation is ran. 
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
			# shouldn't happend 
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

