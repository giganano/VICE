# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport MULTIZONE 

cdef extern from "../src/multizone.h": 
	MULTIZONE *multizone_initialize(unsigned int n) 
	void multizone_free(MULTIZONE *mz) 
	int multizone_evolve(MULTIZONE *mz) 

