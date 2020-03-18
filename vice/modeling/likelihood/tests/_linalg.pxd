# cython: language_level = 3, boundscheck = False 

cdef extern from "../../../src/modeling/likelihood/tests/linalg.h": 
	unsigned short test_add_matrices() 
	unsigned short test_subtract_matrices() 
	unsigned short test_transpose() 
	unsigned short test_determinant() 
	unsigned short test_inversion() 


