# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/io/ccsne.h": 
	unsigned short test_cc_yield_grid(); 
