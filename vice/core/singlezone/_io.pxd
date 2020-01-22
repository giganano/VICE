# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._element cimport ELEMENT 
from . cimport _element 

cdef extern from "../../src/io.h": 
	unsigned short import_agb_grid(ELEMENT *e, char *file) 
