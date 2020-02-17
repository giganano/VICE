# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/ssp/msmf.h": 
	unsigned short test_MSMF() 
