# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from . cimport _singlezone 


cdef class singlezone_tester(c_singlezone): 

	""" 
	This object tests the singlezone object. User access is strongly 
	discouraged. 
	""" 

	def __init__(self): 
		super().__init__(**{}) 
		self._tracker = {} 
		self._names = {} 


	def test(self): 
		""" 
		Run the tests on the singlezone object. 
		""" 
		self._test_address() 
		self._test_n_timesteps() 


	def _test_address(self): 
		""" 
		Test the function which obtains the address of a singlezone object. 
		""" 
		self._tracker["test_address"] = bool(
			_singlezone.test_singlezone_address(self._sz) 
		) 
		self._names["test_address"] = "Address lookup" 


	def _test_n_timesteps(self): 
		""" 
		Test the function which calculates the number of timesteps to allocate 
		memory for 
		""" 
		self._tracker["test_n_timesteps"] = bool(
			_singlezone.test_n_timesteps(self._sz) 
		) 
		self._names["test_n_timesteps"] = "Number of Timesteps"  


