# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/tracer.h": 
	unsigned short test_tracer_initialize() 
	unsigned short test_tracer_free() 
