# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/element.h": 
	unsigned short test_element_initialize() 
	unsigned short test_element_free() 
