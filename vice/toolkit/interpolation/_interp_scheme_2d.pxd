# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ...core.objects._interp_scheme_2d cimport INTERP_SCHEME_2D

cdef class c_interp_scheme_2d:
	cdef INTERP_SCHEME_2D *_is2d


cdef extern from "../../src/objects/interp_scheme_2d.h":
	INTERP_SCHEME_2D *interp_scheme_2d_initialize()
	void interp_scheme_2d_free(INTERP_SCHEME_2D *is2d)


cdef extern from "../../src/toolkit/interp_scheme_2d.h":
	double interp_scheme_2d_evaluate(INTERP_SCHEME_2D is2d, double x, double y)
