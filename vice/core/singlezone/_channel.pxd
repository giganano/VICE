# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._element cimport ELEMENT 

cdef extern from "../../src/objects.h": 
	ctypedef struct CHANNEL: 
		double *yield_ 
		double *grid 
		double *rate 
		double entrainment 

cdef extern from "../../src/channel.h": 
	cdef double CHANNEL_YIELD_GRID_STEP 
	cdef double CHANNEL_YIELD_GRID_MIN 
	cdef double CHANNEL_YIELD_GRID_MAX 
	CHANNEL *channel_initialize() 
	void channel_free(CHANNEL *ch) 
	void normalize_rates(ELEMENT *e, unsigned long length) 
