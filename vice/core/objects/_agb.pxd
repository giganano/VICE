# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import 
from ._callback_2arg cimport CALLBACK_2ARG 
from ._element cimport ELEMENT 


cdef extern from "../../src/objects.h": 
	ctypedef struct AGB_YIELD_GRID: 
		CALLBACK_2ARG *custom_yield 
		double **grid
		double *m
		double *z
		unsigned long n_m
		unsigned long n_z 
		double entrainment 


cdef extern from "../../src/agb.h": 
	AGB_YIELD_GRID *agb_yield_grid_initialize() 
	void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid) 


cdef extern from "../../src/io.h": 
	unsigned short import_agb_grid(ELEMENT *e, char *file) 

