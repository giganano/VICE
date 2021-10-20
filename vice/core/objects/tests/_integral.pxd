# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/integral.h":
	unsigned short test_integral_initialize()
	unsigned short test_integral_free()

