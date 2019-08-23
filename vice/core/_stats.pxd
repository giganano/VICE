# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 

cdef extern from "../src/stats.h": 
	double *sample(double *dist, double *bins, unsigned long n_bins, 
		unsigned long n) 

