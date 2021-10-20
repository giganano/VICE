# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ...core.objects._interp_scheme_1d cimport INTERP_SCHEME_1D

cdef class c_interp_scheme_1d:
	cdef INTERP_SCHEME_1D *_is1d


cdef extern from "../../src/objects/interp_scheme_1d.h":
	INTERP_SCHEME_1D *interp_scheme_1d_initialize()
	void interp_scheme_1d_free(INTERP_SCHEME_1D *is1d)


cdef extern from "../../src/toolkit/interp_scheme_1d.h":
	double interp_scheme_1d_evaluate(INTERP_SCHEME_1D is1d, double x)

