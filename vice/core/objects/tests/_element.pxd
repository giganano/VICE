# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/element.h":
	unsigned short test_element_initialize()
	unsigned short test_element_free()
