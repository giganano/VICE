# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h":
	ctypedef struct TRACER:
		double mass
		int *zone_history
		unsigned int zone_origin
		unsigned int zone_current
		unsigned long timestep_origin


cdef extern from "../../src/multizone/tracer.h":
	TRACER *tracer_initialize()
	void tracer_free(TRACER *t)

