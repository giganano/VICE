# cython: language_level = 3, boundscheck = False 

cdef extern from "../../../src/objects/tests/dataset.h": 
	unsigned short test_dataset_initialize() 
	unsigned short test_dataset_free() 

