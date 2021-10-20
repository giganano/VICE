# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/objects/tests/hydrodiskstars.h":
	unsigned short test_hydrodiskstars_initialize()
	unsigned short test_hydrodiskstars_free()
