# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport SSP, ELEMENT 

cdef extern from "../src/ssp.h": 
	cdef double MASS_LIFETIME_PLAW_INDEX 
	cdef double SOLAR_LIFETIME 
	SSP *ssp_initialize() 
	void ssp_free(SSP *ssp) 
	double *single_population_enrichment(SSP *ssp, ELEMENT *e, 
		double Z, double *times, long n_times, double mstar)
	double CRF(SSP ssp, double time) 
	double MSMF(SSP ssp, double time) 

