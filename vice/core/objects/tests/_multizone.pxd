# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/multizone.h":
	unsigned short test_multizone_initialize()
	unsigned short test_multizone_free()

