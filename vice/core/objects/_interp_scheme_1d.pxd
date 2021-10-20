# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h":
	ctypedef struct INTERP_SCHEME_1D:
		unsigned long n_points
		double *xcoords
		double *ycoords


cdef extern from "../../src/objects/interp_scheme_1d.h":
	INTERP_SCHEME_1D *interp_scheme_1d_initialize()
	void interp_scheme_1d_free(INTERP_SCHEME_1D *is1d)
