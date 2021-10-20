# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._fromfile cimport FROMFILE
from ._fromfile cimport fromfile


cdef extern from "../../src/dataframe/history.h":
	double *history_row(FROMFILE *ff, unsigned long row, char **elements,
		unsigned int n_elements, double *solar, double Z_solar)
	unsigned int history_row_length(FROMFILE *ff, unsigned int n_elements,
		char **elements)
	double *history_lookback(FROMFILE *ff)
	double *history_Z_element(FROMFILE *ff, char *element)
	double *history_logarithmic_abundance_ratio(FROMFILE *ff, char *element1,
		char *element2, char **elements, unsigned int n_elements,
		double *solar)
	double *history_Zscaled(FROMFILE *ff, unsigned int n_elements,
		char **elements, double *solar, double Z_solar)
	double *history_logarithmic_scaled(FROMFILE *ff, unsigned int n_elements,
		char **elements, double *solar)


cdef class history(fromfile):
	cdef char **_elements
	cdef unsigned int _n_elements
	cdef double *_solar
	cdef double _Z_solar

