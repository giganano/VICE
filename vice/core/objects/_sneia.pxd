# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._element cimport ELEMENT
from ._callback_1arg cimport CALLBACK_1ARG


cdef extern from "../../src/objects.h":
	ctypedef struct SNEIA_YIELD_SPECS:
		CALLBACK_1ARG *yield_
		double *RIa
		char *dtd
		double tau_ia
		double t_d
		double entrainment


cdef extern from "../../src/sneia.h":
	cdef double PLAW_DTD_INDEX
	cdef double RIA_MAX_EVAL_TIME
	SNEIA_YIELD_SPECS *sneia_yield_initialize()
	void sneia_yield_free(SNEIA_YIELD_SPECS *sneia_yield)
	void normalize_RIa(ELEMENT *e, unsigned long length)

