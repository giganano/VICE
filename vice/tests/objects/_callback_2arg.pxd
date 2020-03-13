# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/callback_2arg.h": 
	unsigned short test_callback_2arg_initialize() 
	unsigned short test_callback_2arg_free() 

