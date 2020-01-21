# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._elemental_settings cimport elemental_settings 

cdef class channel_entrainment(elemental_settings): 
	pass 

cdef class zone_entrainment: 
	cdef channel_entrainment _agb 
	cdef channel_entrainment _ccsne 
	cdef channel_entrainment _sneia 

