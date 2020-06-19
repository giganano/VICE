# cython: language_level = 3, boundscheck = False 

cdef extern from "../../../src/toolkit/tests/repfunc.h": 
	unsigned short test_repfunc_evaluate() 

