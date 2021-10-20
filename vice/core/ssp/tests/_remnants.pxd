# cython: language_level = 3, boundscheck = False

cdef extern from "../../../src/ssp/tests/remnants.h":
	unsigned short test_Kalirai08_remnant_mass()

