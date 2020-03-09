# cython: language_level = 3, boundscheck = False 


cdef extern from "../../src/objects.h": 
	ctypedef struct CALLBACK_1ARG: 
		double (*callback)(double, void *) 
		void *user_func 

