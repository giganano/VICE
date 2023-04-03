# cython: language_level = 3, boundscheck = False

from ._matrix cimport matrix, matrix_add, matrix_subtract, matrix_multiply

cdef class vector(matrix):
	pass
