# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport FROMFILE 

cdef extern from "../src/history.h": 
	double *history_row(FROMFILE *ff, unsigned long row, char **elements, 
		unsigned int n_elements, double *solar, double Z_solar)
	unsigned int row_length(FROMFILE *ff, unsigned int n_elements)
	double *Z_element(FROMFILE *ff, char *element) 
	double *logarithmic_abundance_ratio(FROMFILE *ff, char *element1, 
		char *element2, char **elements, unsigned int n_elements, 
		double *solar) 
	double *Zscaled(FROMFILE *ff, unsigned int n_elements, char **elements, 
		double *solar, double Z_solar) 
	double *logarithmic_scaled(FROMFILE *ff, unsigned int n_elements, 
		char **elements, double *solar)
