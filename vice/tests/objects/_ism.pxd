# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/ism.h": 
	unsigned short test_ism_initialize() 
	unsigned short test_ism_free() 
