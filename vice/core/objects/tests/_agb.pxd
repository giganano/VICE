# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/agb.h":
	unsigned short test_agb_yield_grid_initialize()
	unsigned short test_agb_yield_grid_free()

