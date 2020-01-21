# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ._objects cimport FROMFILE 

cdef class base: 
	cdef object _frame 

cdef class elemental_settings(base): 
	pass 

cdef class evolutionary_settings(elemental_settings): 
	cdef object _name 

cdef class noncustomizable(elemental_settings): 
	cdef object _name 

cdef class yield_settings(elemental_settings): 
	cdef object __defaults 
	cdef object _allow_funcs 
	cdef object _config_field 

cdef class agb_yield_settings(yield_settings): 
	pass 

cdef class saved_yields(elemental_settings): 
	pass 

cdef class fromfile(base): 
	cdef FROMFILE *_ff 

cdef class history(fromfile): 
	cdef char **_elements 
	cdef unsigned int n_elements 
	cdef double *solar 
	cdef double Z_solar 

# cdef class channel_entrainment(df.elemental_settings): 
# 	pass 



