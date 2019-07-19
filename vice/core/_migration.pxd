# cython: language_level = 3, boundscheck = False 

cdef extern from "../src/migration.h": 
	extern int migration_matrix_sanitycheck(double ***migration_matrix, 
		unsigned long n_times, unsigned int n_zones) 
