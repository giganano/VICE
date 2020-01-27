# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._base cimport base 

cdef class c_configuration(base): 
	cdef object _blockname 
	cdef object _allowed_types 

