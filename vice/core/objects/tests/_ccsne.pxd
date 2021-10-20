# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/ccsne.h":
	unsigned short test_ccsne_yield_initialize()
	unsigned short test_ccsne_yield_free()

