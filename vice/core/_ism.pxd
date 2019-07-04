# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport ISM 

cdef extern from "../src/ism.h": 
	ISM *ism_initialize() 
	void ism_free(ISM *ism) 

