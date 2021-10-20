# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._imf cimport IMF_


cdef extern from "../../src/objects.h":
	ctypedef struct INTEGRAL:
		double (*func)(double)
		double a
		double b
		double tolerance
		unsigned long method
		unsigned long Nmax
		unsigned long Nmin
		unsigned long iters
		double result
		double error


cdef extern from "../../src/objects/integral.h":
	INTEGRAL *integral_initialize()
	void integral_free(INTEGRAL *intgrl)

