# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/mdf.h": 
	unsigned short test_mdf_initialize() 
	unsigned short test_mdf_free() 
