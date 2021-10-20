# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/mdf.h":
	unsigned short test_mdf_initialize()
	unsigned short test_mdf_free()
