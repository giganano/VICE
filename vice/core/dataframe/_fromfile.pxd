# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._base cimport base

cdef extern from "../../src/objects.h": 
	ctypedef struct FROMFILE: 
		char *name 
		char **labels 
		unsigned long n_rows 
		unsigned long n_cols 
		double **data 

cdef extern from "../../src/fromfile.h": 
	FROMFILE *fromfile_initialize() 
	void fromfile_free(FROMFILE *ff) 
	unsigned short fromfile_read(FROMFILE *ff) 
	double *fromfile_column(FROMFILE *ff, char *label)  
	unsigned short fromfile_modify_column(FROMFILE *ff, char *label, 
		double *arr) 
	unsigned short fromfile_new_column(FROMFILE *ff, char *label, double *arr) 
	double *fromfile_row(FROMFILE *ff, unsigned long row) 

cdef class fromfile(base): 
	cdef FROMFILE *_ff 

