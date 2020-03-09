# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._callback_1arg cimport CALLBACK_1ARG 


cdef extern from "../../src/objects.h": 
	ctypedef struct IMF_: 
		char *spec 
		double m_lower 
		double m_upper 
		double *mass_distribution 
		CALLBACK_1ARG *custom_imf 


cdef extern from "../../src/imf.h": 
	IMF_ *imf_initialize() 
	void imf_free(IMF_ *imf) 
	unsigned short imf_set_mass_distribution(IMF_ *imf, double *arr) 
	unsigned long n_mass_bins(IMF_ *imf) 
	unsigned long imf_evaluate(IMF_ imf, double m) 
	double salpeter55(double m) 
	double kroupa01(double m) 


