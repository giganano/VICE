# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._element cimport ELEMENT
from ..objects._ssp cimport SSP
from ..objects._ssp cimport ssp_initialize
from ..objects._ssp cimport ssp_free


cdef extern from "../../src/ssp.h":
	double *single_population_enrichment(SSP *ssp, ELEMENT *e,
		double Z, double *times, unsigned long n_times, double mstar)
	double CRF(SSP ssp, double time)
	double MSMF(SSP ssp, double time)

