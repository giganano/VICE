# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport MULTIZONE 
from ._objects cimport TRACER 

cdef extern from "../src/tracer.h": 
	TRACER *tracer_initialize() 
	void tracer_free(TRACER *t) 
	void malloc_tracers(MULTIZONE *mz) 
	# unsigned short setup_zone_history(MULTIZONE mz, TRACER *t, 
	# 	unsigned long origin, unsigned long final, unsigned long birth) 

