# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._noncustomizable cimport noncustomizable 

cdef class builtin_elemental_data(noncustomizable): 
	pass 

