# cython: language_level = 3, boundscheck = False 
""" 
This file handles the implementation of the migration matrix. 
""" 

from __future__ import absolute_import 
from . import _pyutils 
import numbers 
import sys 
import os 

class migration_matrix(object): 

	""" 
	Contains user-specified migration prescriptions for use in multizone 
	simulations. For a multizone simulation with N zones, this is an NxN 
	matrix. 

	This matrix is defined such that the ij'th element represents the 
	likelihood that interstellar gas or stars will migrate FROM the i'th TO 
	the j'th zone in the simulation. These entries may be either numerical 
	values or functions of time in Gyr. In all cases, the value at a given 
	time must be between 0 and 1, because the elements are interpreted as 
	likelihoods. 
	""" 

	def __init__(self, size): 
		# multizone object will perform this type-checking 
		assert isinstance(size, int), "Must be an integer number of zones." 
		assert size > 0, "Negative number of zones" 

		self._rows = size * [None] 
		for i in range(size): 
			self._rows[i] = row(size) 

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
		The number of zones in the simulation. 
		""" 
		return self._rows[0].dimension 



class row(object): 

	""" 
	A row of the migration matrix. For a multizone simulation with N zones, 
	this is an N-element list. 

	This row is defined such that the i'th element represents the likelihood 
	that interstellar gas or stars will migrate FROM this zone TO the i'th 
	zone in the simulation. These entries may be either numerical value or 
	functions of time in Gyr. In all cases, the value at a given time must be 
	between 0 and 1, because the elements are interpreted as likelihoods. 
	""" 

	def __init__(self, dimension): 
		self.dimension = dimension 
		self._row = self.dimension * [0.0] 

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
		if isinstance(key, int): 
			# user passed the proper type 
			if isinstance(value, numbers.Number): 
				# probability of migration must be between 0 and 1 
				if 0 <= value <= 1: 
					self._row[key] = float(value) 
				else: 
					raise ValueError("""Numerical element of migration matrix \
must be between 0 and 1 (inclusive). Got: %g""" % (value)) 
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
	If key is an integer between 0 and maximum - 1, the key itself. Otherwise, 
	a list whose 0th element is the exception type and whose second element is 
	the message. 
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


