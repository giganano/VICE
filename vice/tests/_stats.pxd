# cython: language_level = 3, boundscheck = False 

cdef extern from "../src/tests/stats.h": 
	unsigned short test_normal() 
	unsigned short test_convert_to_PDF() 
