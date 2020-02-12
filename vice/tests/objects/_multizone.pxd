# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/multizone.h": 
	unsigned short test_multizone_initialize() 
	unsigned short test_multizone_free() 

