# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/ssp.h": 
	unsigned short test_ssp_initialize() 
	unsigned short test_ssp_free() 
