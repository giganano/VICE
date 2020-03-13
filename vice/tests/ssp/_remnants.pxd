# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/ssp/remnants.h": 
	unsigned short test_Kalirai08_remnant_mass() 

