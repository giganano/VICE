# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport SNEIA_YIELD_SPECS, ELEMENT 

cdef extern from "../src/sneia.h": 
	cdef double PLAW_DTD_INDEX 
	cdef double RIA_MAX_EVAL_TIME 
	SNEIA_YIELD_SPECS *sneia_yield_initialize() 
	void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yield) 
	void normalize_RIa(ELEMENT *e, unsigned long length) 


