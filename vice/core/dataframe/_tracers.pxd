# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._history cimport history 
from ._fromfile cimport FROMFILE 

cdef class tracers(history): 
	pass 


cdef extern from "../../src/dataframe/tracers.h": 
	double *tracers_ages(FROMFILE *ff) 
	double *tracers_Z_element(FROMFILE *ff, char *element) 
	double *tracers_log_abundance_ratio(FROMFILE *ff, char *element1, 
		char *element2, char **elements, unsigned int n_elements, double *solar) 
	double *tracers_Zscaled(FROMFILE *ff, unsigned int n_elements, 
		char **elements, double *solar, double Z_solar) 
	double *tracers_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements, 
		char **elements, double *solar) 

