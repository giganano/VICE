# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/imf.h":
	unsigned short test_imf_initialize()
	unsigned short test_imf_free()

