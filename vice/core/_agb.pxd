# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport AGB_YIELD_GRID 

cdef extern from "../src/agb.h": 
	AGB_YIELD_GRID *agb_yield_grid_initialize() 
	void agb_yield_grid_free(AGB_YIELD_GRID *agb_grid) 
	

