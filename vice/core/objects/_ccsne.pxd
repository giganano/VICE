# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._callback_1arg cimport CALLBACK_1ARG


cdef extern from "../../src/ccsne.h":
	ctypedef struct CCSNE_YIELD_SPECS:
		CALLBACK_1ARG *yield_
		double entrainment


cdef extern from "../../src/ccsne.h":
	double CC_MIN_STELLAR_MASS
	CCSNE_YIELD_SPECS *ccsne_yield_initialize()
	void ccsne_yield_free(CCSNE_YIELD_SPECS *ccsne_yield)
	double *IMFintegrated_fractional_yield_numerator(char *file, char *IMF,
		double m_lower, double m_upper, double tolerance, char *method,
		unsigned long Nmax, unsigned long Nmin)
	double *IMFintegrated_fractional_yield_denominator(char *IMF,
		double m_lower, double m_upper, double tolerance, char *method,
		unsigned long Nmax, unsigned long Nmin)


