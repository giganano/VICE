# cython: language_level = 3, boundscheck = False 
""" 
This file contains the declarations for the singlezone and multizone objects. 
""" 

from ._objects cimport SINGLEZONE 
from ._objects cimport MULTIZONE 

cdef class c_singlezone: 
	cdef SINGLEZONE *_sz 
	cdef object _func 
	cdef object _eta 
	cdef object _enhancement 
	cdef object _tau_star 
	cdef object _zin 
	cdef object _ria 
	cdef double _Mg0 
	cdef object _agb_model 

cdef class migration_specifications: 
	cdef object _stars 
	cdef object _gas 

cdef class multizone: 
	cdef MULTIZONE *_mz 
	cdef c_singlezone *_zones 
	cdef migration_specifications _migration 

