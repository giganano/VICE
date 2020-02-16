# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/ssp/crf.h": 
	unsigned short test_CRF() 

