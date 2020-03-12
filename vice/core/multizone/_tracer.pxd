# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from . cimport _tracer 
from . cimport _multizone 


cdef extern from "../../src/objects.h": 
	ctypedef struct TRACER: 
		double mass 
		int *zone_history 
		unsigned int zone_origin 
		unsigned int zone_current 
		unsigned int timestep_origin 


cdef extern from "../../src/multizone/tracer.h": 
	void malloc_tracers(_multizone.MULTIZONE *mz) 


