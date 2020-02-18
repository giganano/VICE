# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/io/agb.h": 
	unsigned short test_import_agb_grid() 

