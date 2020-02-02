# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ...core.singlezone._singlezone cimport c_singlezone 
from ._dataset cimport dataset 

cdef class c_singlechain: 
	cdef c_singlezone _sz 
	cdef dataset _data 
	cdef object _eta 
	cdef object _enhancement 
	cdef object _recycling 
	cdef object _delay 
	cdef object _Mg0 
	cdef object _smoothing 
	cdef object _tau_ia 
	cdef object _tau_star 
	cdef object _schmidt_index 
	cdef object _m_upper 
	cdef object _m_lower 

