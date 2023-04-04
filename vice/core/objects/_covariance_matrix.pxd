# cython: language_level = 3, boundscheck = False

from ._matrix cimport MATRIX

cdef extern from "../../src/objects.h":
	ctypedef struct COVARIANCE_MATRIX:
		double **matrix
		unsigned short n_rows
		unsigned short n_cols
		MATRIX *inv
