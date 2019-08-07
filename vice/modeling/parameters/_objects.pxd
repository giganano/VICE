# cython: language_level = 3, boundscheck = False
""" 
This file wraps the C objects scripted in vice/src/objects.h. Their 
documentation is not duplicated here. See their source code for more details.  
""" 

from libc.stdio cimport FILE 

cdef extern from "../../src/objects.h": 
	ctypedef struct NUMPARAM: 
		FILE *output 
		unsigned short varies 
		double stepsize 
		double current 

