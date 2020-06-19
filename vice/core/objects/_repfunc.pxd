# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 

cdef extern from "../../src/objects.h": 
	ctypedef struct REPFUNC: 
		unsigned long n_points 
		double *xcoords 
		double *ycoords 


cdef extern from "../../src/objects/repfunc.h": 
	REPFUNC *repfunc_initialize() 
	void repfunc_free(REPFUNC *rpf) 

