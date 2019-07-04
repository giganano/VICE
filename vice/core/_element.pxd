# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport ELEMENT 

cdef extern from "../src/element.h": 
	ELEMENT *element_initialize() 
	void element_free(ELEMENT *e) 

