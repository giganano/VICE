# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/fromfile.h": 
	unsigned short test_fromfile_initialize() 
	unsigned short test_fromfile_free() 
