# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...core.singlezone._singlezone cimport SINGLEZONE, c_singlezone 

cdef extern from "../../src/tests/singlezone/singlezone.h": 
	unsigned short test_singlezone_address(SINGLEZONE *test) 
	unsigned short test_n_timesteps(SINGLEZONE *test) 
	unsigned short test_singlezone_stellar_mass(SINGLEZONE *test) 


cdef class singlezone_tester(c_singlezone): 
	cdef object _tracker 
	cdef object _names 

