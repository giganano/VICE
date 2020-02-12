# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/dataset.h": 
	unsigned short test_dataset_initialize() 
	unsigned short test_dataset_free() 

