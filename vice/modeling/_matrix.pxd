# cython: language_level = 3, boundscheck = False

from ..core.objects._matrix cimport MATRIX, matrix_initialize, matrix_free

cdef extern from "../src/modeling/matrix.h":
	MATRIX *matrix_multiply(MATRIX m1, MATRIX m2, MATRIX *result)
	MATRIX *matrix_invert(MATRIX m, MATRIX *result)
	MATRIX *matrix_transpose(MATRIX m, MATRIX *result)
	double matrix_determinant(MATRIX m)


cdef class c_matrix:
	cdef MATRIX *_m
