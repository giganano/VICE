# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/callback_1arg.h": 
	unsigned short test_callback_1arg_initialize() 
	unsigned short test_callback_1arg_free() 

