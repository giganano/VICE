# cython: language_level = 3, boundscheck = False

from ._objects cimport POLYNOMIAL 
cdef extern from "../../src/polynomial.h": 
	POLYNOMIAL *polynomial_initialize(unsigned short n) 
	void polynomial_free(POLYNOMIAL *poly) 
	double polynomial_evaluate(POLYNOMIAL poly, double x) 

