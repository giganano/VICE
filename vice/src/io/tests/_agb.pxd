# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/io/tests/agb.h":
	unsigned short test_import_agb_grid()

