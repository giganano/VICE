# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/utils.h": 
	void seed_random() 


