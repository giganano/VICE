# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._parameters cimport parameters 
from ._stepsizes cimport stepsizes 

cdef class fitting_function: 
	cdef object _func 
	cdef parameters _parameters 
	cdef stepsizes _stepsizes 
	cdef int _n 
