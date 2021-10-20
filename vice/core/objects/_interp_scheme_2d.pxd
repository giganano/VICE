# cython: language_level = 3, boundscheck = False

cdef extern from "../../src/objects.h":
	ctypedef struct INTERP_SCHEME_2D:
		unsigned long n_x_values
		unsigned long n_y_values
		double *xcoords
		double *ycoords
		double **zcoords


cdef extern from "../../src/objects/interp_scheme_2d.h":
	INTERP_SCHEME_2D *interp_scheme_2d_initialize()
	void interp_scheme_2d_free()
