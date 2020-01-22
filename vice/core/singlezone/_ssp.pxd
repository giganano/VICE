# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._element cimport ELEMENT 
from ._imf cimport IMF_ 

cdef extern from "../../src/objects.h": 
	ctypedef struct SSP: 
		IMF_ *imf 
		double *crf 
		double *msmf 
		double postMS 
		double R0 
		int continuous 

cdef extern from "../../src/ssp.h": 
	cdef double MASS_LIFETIME_PLAW_INDEX 
	cdef double SOLAR_LIFETIME 
	SSP *ssp_initialize() 
	void ssp_free(SSP *ssp) 
	double main_sequence_turnoff_mass(double t, double postMS) 
	double *single_population_enrichment(SSP *ssp, ELEMENT *e, 
		double Z, double *times, unsigned long n_times, double mstar)
	double CRF(SSP ssp, double time) 
	double MSMF(SSP ssp, double time) 

