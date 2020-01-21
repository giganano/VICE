# cython: language_level = 3, boundscheck = False 

from . cimport _dataframe as df 

cdef class channel_entrainment(df.elemental_settings): 
	pass 

cdef class zone_entrainment: 
	cdef channel_entrainment _agb 
	cdef channel_entrainment _ccsne 
	cdef channel_entrainment _sneia 
