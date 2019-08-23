# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport SINGLEZONE 

cdef extern from "../src/singlezone.h": 
	double SINGLEZONE_MAX_EVAL_TIME
	SINGLEZONE *singlezone_initialize() 
	void singlezone_free(SINGLEZONE *sz) 
	long singlezone_address(SINGLEZONE *sz) 
	unsigned short singlezone_evolve(SINGLEZONE *sz) 
	void singlezone_cancel(SINGLEZONE *sz) 
	unsigned long n_timesteps(SINGLEZONE sz) 

