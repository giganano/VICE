# cython: language_level = 3, boundscheck = False 

cdef class parameters: 
	cdef object _parameters 

cdef extern from "../../src/stats.h": 
	double normal(double mean, double sigma) 

cdef extern from "../../src/utils.h": 
	void seed_random() 

