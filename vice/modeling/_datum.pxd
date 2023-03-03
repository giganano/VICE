# cython: language_level = 3, boundscheck = False

from ..core.objects._matrix cimport MATRIX, matrix_initialize, matrix_free
from ..core.objects._datum cimport DATUM, datum_initialize, datum_free
from ..core.dataframe._base cimport base as dataframe


cdef extern from "../src/objects/datum.h":
	void link_cov_matrix(DATUM *d, char *address)


cdef class c_datum(dataframe):
	cdef DATUM *_d
	cdef object _cov

