# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._parameters cimport parameters 

cdef class fitting_function: 
	cdef object _function 
	cdef parameters _parameters 
	cdef int _n 
