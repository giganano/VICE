# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._engine cimport engine 

cdef class E16(engine): 
	cdef double *_m4 
	cdef double *_mu4 
	cdef double _slope 
	cdef double _intercept 

