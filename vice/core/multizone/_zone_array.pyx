# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..._globals import _RECOGNIZED_ELEMENTS_
from ..singlezone import singlezone
import numbers
from . cimport _zone_array

cdef class zone_array:

	"""
	An object indexable by integers which only allows singlezone objects to be
	stored. These objects will only be created automatically upon
	initialization of a multizone object.

	.. versionadded:: 1.2.0
	"""

	def __init__(self, n):
		assert isinstance(n, int), "Internal Error"
		self._n = n
		self._zones = n * [None]
		for i in range(n):
			self._zones[i] = singlezone()
			self._zones[i].name = "zone%d" % (i)

	def __len__(self):
		return self._n

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
		self.__copy_entrainment_settings(key, sz)
		self._zones[key].agb_model 			= sz.agb_model
		self._zones[key].bins 				= sz.bins
		self._zones[key].delay 				= sz.delay
		self._zones[key].dt 				= sz.dt
		self._zones[key].RIa 				= sz.RIa
		self._zones[key].elements 			= sz.elements
		self._zones[key].enhancement 		= sz.enhancement
		self._zones[key].eta 				= sz.eta
		self._zones[key].func 				= sz.func
		self._zones[key].IMF 				= sz.IMF
		self._zones[key].m_lower 			= sz.m_lower
		self._zones[key].m_upper 			= sz.m_upper
		self._zones[key].Mg0 				= sz.Mg0
		self._zones[key].MgSchmidt 			= sz.MgSchmidt
		self._zones[key].mode 				= sz.mode
		self._zones[key].name 				= sz.name
		self._zones[key].postMS				= sz.postMS
		self._zones[key].recycling 			= sz.recycling
		self._zones[key].RIa 				= sz.RIa
		self._zones[key].schmidt 			= sz.schmidt
		self._zones[key].schmidt_index 		= sz.schmidt_index
		self._zones[key].smoothing 			= sz.smoothing
		self._zones[key].tau_ia 			= sz.tau_ia
		self._zones[key].tau_star 			= sz.tau_star
		self._zones[key].Z_solar 			= sz.Z_solar
		self._zones[key].Zin 				= sz.Zin

	def __copy_entrainment_settings(self, key, sz):
		"""
		Copies the entrainment settings into the new zone
		"""
		assert isinstance(key, int), "Internal Error"
		assert isinstance(sz, singlezone), "Internal Error"
		for i in _RECOGNIZED_ELEMENTS_:
			self._zones[key].entrainment.agb[i] = sz.entrainment.agb[i]
			self._zones[key].entrainment.ccsne[i] = sz.entrainment.ccsne[i]
			self._zones[key].entrainment.sneia[i] = sz.entrainment.sneia[i]

