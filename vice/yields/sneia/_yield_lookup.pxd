# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/io/sneia.h":
	double single_ia_mass_yield_lookup(char *file)
