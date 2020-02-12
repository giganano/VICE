# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/integral.h": 
	unsigned short test_integral_initialize() 
	unsigned short test_integral_free() 

