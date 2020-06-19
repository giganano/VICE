# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
from ...core.objects._repfunc cimport REPFUNC 

cdef class c_repfunc: 
	cdef REPFUNC *_rpf 


cdef extern from "../../src/objects/repfunc.h": 
	REPFUNC *repfunc_initialize() 
	void repfunc_free(REPFUNC *rpf) 


cdef extern from "../../src/toolkit/repfunc.h": 
	double repfunc_evaluate(REPFUNC rpf, double x) 

