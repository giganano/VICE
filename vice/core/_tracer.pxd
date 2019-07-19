# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects import TRACER 

cdef extern from "../src/tracer.h": 
	TRACER *tracer_initialize() 
	void tracer_free(TRACER *t) 
