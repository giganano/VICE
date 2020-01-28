# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._stepsizes cimport stepsizes 

cdef class parameters(stepsizes): 
	cdef object _old 

cdef extern from "../../src/stats.h": 
	double normal(double mean, double sigma) 

cdef extern from "../../src/utils.h": 
	void seed_random() 

