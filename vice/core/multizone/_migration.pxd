# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._multizone cimport MULTIZONE


cdef extern from "../../src/multizone/migration.h":
	void malloc_gas_migration(MULTIZONE *mz)
	unsigned short setup_migration_element(MULTIZONE mz,
		double ***migration_matrix, unsigned int row, unsigned int column,
		double *arr)


cdef class mig_matrix:
	cdef object _rows


cdef class mig_matrix_row:
	cdef int _size
	cdef object _row


cdef class mig_specs:
	cdef object _stars
	cdef mig_matrix _gas

