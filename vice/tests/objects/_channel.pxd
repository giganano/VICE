# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/channel.h": 
	unsigned short test_channel_initialize() 
	unsigned short test_channel_free() 

