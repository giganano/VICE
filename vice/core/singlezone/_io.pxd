# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from . cimport _element 

cdef extern from "../../src/io.h": 
	unsigned short import_agb_grid(_element.ELEMENT *e, char *file) 
