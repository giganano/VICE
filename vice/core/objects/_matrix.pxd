# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h":
	ctypedef struct MATRIX:
		double **matrix
		unsigned short n_rows
		unsigned short n_cols

cdef extern from "../../src/objects/matrix.h":
	MATRIX *matrix_initialize(unsigned short n_rows, unsigned short n_cols)
	void matrix_free(MATRIX *m)

