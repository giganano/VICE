# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport ELEMENT 

cdef extern from "../src/io.h": 
	cdef double LINESIZE 
	cdef double MAX_FILENAME_SIZE 
	double **read_square_ascii_file(char *file) 
	int header_length(char *file) 
	int file_dimension(char *file) 
	long line_count(char *file) 
	int import_agb_grid(ELEMENT *e, char *file) 
	int single_ia_mass_yield_lookup(char *file) 



