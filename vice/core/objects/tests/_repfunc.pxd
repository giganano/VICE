# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/repfunc.h": 
	unsigned short test_repfunc_initialize() 
	unsigned short test_repfunc_free() 

