# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
from ...core.objects._callback_1arg cimport CALLBACK_1ARG 
from ...core.objects._integral cimport INTEGRAL 
from ...core.objects._imf cimport IMF_ 


cdef extern from "../../src/yields/ccsne.h": 
	unsigned short IMFintegrated_fractional_yield_numerator(
		INTEGRAL *intgrl, IMF_ *imf, CALLBACK_1ARG *explodability, 
		char *file) 
	extern unsigned short IMFintegrated_fractional_yield_denominator(
		INTEGRAL *intgrl, IMF_ *imf) 

