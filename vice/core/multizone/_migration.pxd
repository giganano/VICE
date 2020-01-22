# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from libc.stdio cimport FILE 
from . cimport _tracer 
from . cimport _multizone

cdef extern from "../../src/objects.h": 
	ctypedef struct MIGRATION: 
		unsigned int n_zones 
		unsigned int n_tracers 
		unsigned long tracer_count 
		double ***gas_migration 
		_tracer.TRACER **tracers 
		FILE *tracers_output 

cdef extern from "../../src/migration.h": 
	void malloc_gas_migration(_multizone.MULTIZONE *mz) 
	unsigned short setup_migration_element(_multizone.MULTIZONE mz, 
		double ***migration_matrix, unsigned int row, unsigned int column, 
		double *arr) 

cdef class mig_matrix: 
	cdef object _rows 

cdef class mig_matrix_row: 
	cdef int _dimension 
	cdef object _row 

cdef class mig_specs: 
	cdef object _stars 
	cdef mig_matrix _gas 


