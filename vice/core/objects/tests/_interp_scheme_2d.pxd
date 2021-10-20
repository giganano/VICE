# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/interp_scheme_2d.h":
	unsigned short test_interp_scheme_2d_initialize()
	unsigned short test_interp_scheme_2d_free()
