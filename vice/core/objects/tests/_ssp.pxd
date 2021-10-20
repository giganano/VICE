# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/ssp.h":
	unsigned short test_ssp_initialize()
	unsigned short test_ssp_free()
