# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/ssp/mlr.h": 
	unsigned short test_main_sequence_turnoff_mass() 
