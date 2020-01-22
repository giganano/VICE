# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..singlezone import singlezone 
import numbers 
from . cimport _zone_array 

cdef class zone_array: 

	""" 
	An object indexable by integers which only allows singlezone objects to be 
	stored. These objects will only be created automatically upon 
	initialization of a multizone object. 
	""" 

	def __init__(self, n): 
		assert isinstance(n, int), "Internal Error" 
		self._n = n 
		self._zones = n * [None] 
		for i in range(n): 
			self._zones[i] = singlezone() 
			self._zones[i].name = "zone%d" % (i) 

	def __getitem__(self, key): 
		""" 
		Allow indexing by key of type int 
		""" 
		if isinstance(key, numbers.Number): 
			if 0 <= key < self._n: 
				if key % 1 == 0: 
					return self._zones[int(key)] 
				else: 
					raise IndexError("""Index must be interpretable as an \
integer. Got: %g""" % (key)) 
			else: 
				raise IndexError("Index out of bounds: %g" % (key)) 
		else: 
			raise IndexError("Index must be an integer. Got: %s" % (type(key))) 

	def __setitem__(self, key, value): 
		""" 
		Allow indexing by key of type int; item must be of type singlezone 
		""" 
		if isinstance(key, numbers.Number): 
			if 0 <= key < self._n: 
				if key % 1 == 0: 
					if isinstance(value, singlezone): 
						""" 
						Because the memory addresses of each singlezone object 
						is copied into the multizone object, must instead copy 
						each attribute here, preventing memory errors 
						""" 
						self.__copy_attributes(int(key), value) 
					else: 
						raise TypeError("""Item must be of type singlezone. \
Got: %s""" % (type(value))) 
				else: 
					raise ValueError("""Index must be interpretable as an \
integer. Got: %g""" % (key)) 
			else: 
				raise ValueError("Index out of bounds: %g" % (key)) 
		else: 
			raise TypeError("Index must be an integer. Got: %s" % (type(key))) 

	def __repr__(self): 
		return str([self._zones[i] for i in range(self._n)]) 

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
		return self.exc_value is None 

	def __copy_attributes(self, key, sz): 
		""" 
		Copies the attributes of singlezone object sz into the zone at index 
		key 
		""" 
		assert isinstance(key, int), "Internal Error" 
		assert isinstance(sz, singlezone), "Internal Error" 
		self._zones[int(key)].agb_model 		= sz.agb_model
		self._zones[int(key)].bins 				= sz.bins
		self._zones[int(key)].delay 			= sz.delay
		self._zones[int(key)].dt 				= sz.dt
		self._zones[int(key)].RIa 				= sz.RIa
		self._zones[int(key)].elements 			= sz.elements
		self._zones[int(key)].enhancement 		= sz.enhancement 
		self._zones[int(key)].entrainment 		= sz.entrainment 
		self._zones[int(key)].eta 				= sz.eta
		self._zones[int(key)].func 				= sz.func
		self._zones[int(key)].IMF 				= sz.IMF
		self._zones[int(key)].m_lower 			= sz.m_lower
		self._zones[int(key)].m_upper 			= sz.m_upper
		self._zones[int(key)].Mg0 				= sz.Mg0
		self._zones[int(key)].MgSchmidt 		= sz.MgSchmidt
		self._zones[int(key)].mode 				= sz.mode
		self._zones[int(key)].name 				= sz.name 
		self._zones[int(key)].postMS			= sz.postMS 
		self._zones[int(key)].recycling 		= sz.recycling 
		self._zones[int(key)].RIa 				= sz.RIa 
		self._zones[int(key)].schmidt 			= sz.schmidt
		self._zones[int(key)].schmidt_index 	= sz.schmidt_index
		self._zones[int(key)].smoothing 		= sz.smoothing
		self._zones[int(key)].tau_ia 			= sz.tau_ia
		self._zones[int(key)].tau_star 			= sz.tau_star 
		self._zones[int(key)].Z_solar 			= sz.Z_solar
		self._zones[int(key)].Zin 				= sz.Zin


