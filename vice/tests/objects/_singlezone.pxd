# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/singlezone.h": 
	unsigned short test_singlezone_initialize() 
	unsigned short test_singlezone_free() 
