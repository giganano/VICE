# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/sneia.h": 
	unsigned short test_sneia_yield_initialize() 
	unsigned short test_sneia_yield_free() 
