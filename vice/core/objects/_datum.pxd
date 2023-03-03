# cython: language_level = 3, boundscheck = False

from ._matrix cimport MATRIX

cdef extern from "../../src/objects.h":
	ctypedef struct DATUM:
		double **data
		unsigned short n_rows
		unsigned short n_cols
		char **labels
		MATRIX *cov
		MATRIX *invcov

cdef extern from "../../src/objects/datum.h":
	DATUM *datum_initialize(unsigned short dim)
	void datum_free(DATUM *d)
