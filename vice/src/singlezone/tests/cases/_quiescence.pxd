# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from .....core.singlezone._singlezone cimport c_singlezone 
from .....core.objects._singlezone cimport SINGLEZONE 

cdef class quiescence(c_singlezone): 
	pass 


cdef extern from "../../singlezone.h": 
	unsigned short singlezone_setup(SINGLEZONE *sz) 
	void singlezone_evolve_no_setup_no_clean(SINGLEZONE *sz) 


cdef extern from "../../mdf.h": 
	void normalize_MDF(SINGLEZONE *sz) 


cdef extern from "../../../io/singlezone.h": 
	void write_mdf_output(SINGLEZONE sz) 


cdef extern from "../agb.h": 
	unsigned short quiescence_test_m_AGB(SINGLEZONE *sz) 

