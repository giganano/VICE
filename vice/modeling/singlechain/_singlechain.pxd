# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...core.singlezone._singlezone cimport c_singlezone 

cdef class c_singlechain: 
	cdef c_singlezone _sz 

