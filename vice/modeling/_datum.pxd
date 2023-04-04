# cython: language_level = 3, boundscheck = False

from ..core.objects._matrix cimport MATRIX, matrix_initialize, matrix_free
from ..core.objects._datum cimport DATUM, datum_initialize, datum_free
from ..core.objects._covariance_matrix cimport COVARIANCE_MATRIX
from ..core.dataframe._base cimport base as dataframe
from ._vector cimport vector
from ._matrix cimport matrix


cdef extern from "../src/objects/datum.h":
	void link_cov_matrix(DATUM *d, char *address)


cdef class datavector(vector):
	cdef DATUM *_d
	cdef covariance_matrix _cov
	cdef datum_keys _keys


cdef class datum_keys:
	cdef char **_keys
	cdef unsigned short _n_keys


cdef class covariance_matrix(matrix):
	cdef COVARIANCE_MATRIX *_cov
	cdef matrix _inv

