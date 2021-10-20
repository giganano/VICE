# cython: language_level = 3, boundscheck = False


cdef extern from "../../src/imf.h":
	double salpeter55(double m)
	double kroupa01(double m)

