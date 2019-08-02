# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport FROMFILE 

cdef extern from "../src/fromfile.h": 
	FROMFILE *fromfile_initialize() 
	void fromfile_free(FROMFILE *ff) 
	int fromfile_read(FROMFILE *ff) 
	double *fromfile_column(FROMFILE *ff, char *label)  
	int fromfile_modify_column(FROMFILE *ff, char *label, double *arr) 
	int fromfile_new_column(FROMFILE *ff, char *label, double *arr) 
	double *fromfile_row(FROMFILE *ff, unsigned long row) 
