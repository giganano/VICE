# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport MULTIZONE 

cdef extern from "../src/migration.h": 
	void malloc_gas_migration(MULTIZONE *mz) 
	unsigned short setup_migration_element(MULTIZONE mz, 
		double ***migration_matrix, unsigned int row, unsigned int column, 
		double *arr) 
	
