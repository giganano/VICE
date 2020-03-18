# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...objects._singlezone cimport SINGLEZONE 
from ...objects._element cimport ELEMENT 
from .._singlezone cimport c_singlezone 


cdef extern from "../../src/singlezone/tests.h": 
	unsigned short test_singlezone_address(SINGLEZONE *test) 
	unsigned short test_n_timesteps(SINGLEZONE *test) 
	unsigned short test_singlezone_stellar_mass(SINGLEZONE *test) 


cdef class singlezone_tester(c_singlezone): 
	pass 

