# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from libc.stdio cimport FILE 
from ..dataframe._entrainment cimport zone_entrainment 
from . cimport _element 
from . cimport _ism 
from . cimport _mdf 
from . cimport _ssp 

cdef extern from "../../src/objects.h": 
	ctypedef struct SINGLEZONE: 
		char *name 
		FILE *history_writer 
		FILE *mdf_writer 
		double dt 
		double current_time 
		double *output_times 
		unsigned long timestep 
		unsigned long n_outputs 
		double Z_solar 
		unsigned int n_elements 
		unsigned short verbose 
		_element.ELEMENT **elements 
		_ism.ISM *ism 
		_mdf.MDF *mdf 
		_ssp.SSP *ssp 


cdef extern from "../../src/singlezone.h": 
	double SINGLEZONE_MAX_EVAL_TIME 
	long BUFFER 
	SINGLEZONE *singlezone_initialize() 
	void singlezone_free(SINGLEZONE *sz) 
	long singlezone_address(SINGLEZONE *sz) 
	unsigned short singlezone_evolve(SINGLEZONE *sz) 
	void singlezone_cancel(SINGLEZONE *sz) 
	unsigned long n_timesteps(SINGLEZONE sz) 


cdef class c_singlezone: 
	cdef SINGLEZONE *_sz 
	cdef object _func 
	cdef object _imf 
	cdef object _eta 
	cdef object _enhancement 
	cdef zone_entrainment _entrainment 
	cdef object _tau_star 
	cdef object _zin 
	cdef object _ria 
	cdef double _Mg0 
	cdef object _agb_model 

