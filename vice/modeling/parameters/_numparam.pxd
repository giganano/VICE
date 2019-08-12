# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
from ._objects cimport NUMPARAM 

cdef extern from "../../src/numparam.h": 
	NUMPARAM *numparam_initialize(double start, unsigned short let_vary) 
	void numparam_free(NUMPARAM *p) 
	void numparam_step(NUMPARAM *p) 
	void numparam_address(NUMPARAM *p) 

