# cython: language_level = 3, boundscheck = False 

cdef extern from "../../../../src/ccsne.h": 
	double CC_MIN_STELLAR_MASS 

cdef extern from "../../../../src/utils.h": 
	double interpolate(double x1, double x2, double y1, double y2, double x) 
	long get_bin_number(double *binspace, unsigned long num_bins, double value) 

cdef class engine: 
	cdef double *_masses 
	cdef double *_frequencies 
	cdef unsigned long _n_masses 
