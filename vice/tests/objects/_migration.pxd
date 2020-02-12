# cython: language_level = 3, boundscheck = False 

cdef extern from "../../src/tests/objects/migration.h": 
	unsigned short test_migration_initialize() 
	unsigned short test_migration_free() 
