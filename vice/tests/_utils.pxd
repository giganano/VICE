# cython: language_level = 3, boundscheck = False 

cdef extern from "../src/tests/utils.h": 
	unsigned short test_choose() 
	unsigned short test_absval() 
	unsigned short test_sign() 
	unsigned short test_simple_hash() 
	unsigned short test_rand_range() 
	unsigned short test_interpolate() 
	unsigned short test_interpolate2D() 
	unsigned short test_get_bin_number() 
	unsigned short test_binspace() 
