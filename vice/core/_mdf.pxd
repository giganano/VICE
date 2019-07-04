# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport MDF 

cdef extern from "../src/mdf.h": 
	MDF *mdf_initialize() 
	void mdf_free(MDF *mdf) 

