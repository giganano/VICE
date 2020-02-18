# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/io/sneia.h": 
	unsigned short test_single_ia_mass_yield_lookup() 
