# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..singlezone cimport _singlezone 
from . cimport _migration 
from . cimport _zone_array 

cdef extern from "../../src/objects.h": 
	ctypedef struct MULTIZONE: 
		char *name 
		_singlezone.SINGLEZONE **zones 
		_migration.MIGRATION *mig 
		unsigned short verbose 
		unsigned short simple 

cdef extern from "../../src/multizone.h": 
	MULTIZONE *multizone_initialize(unsigned int n) 
	void multizone_free(MULTIZONE *mz) 
	void link_zone(MULTIZONE *mz, unsigned long address, 
		unsigned int zone_index) 
	unsigned short multizone_evolve(MULTIZONE *mz) 
	void multizone_cancel(MULTIZONE *mz) 

cdef class c_multizone: 
	cdef MULTIZONE *_mz 
	cdef _zone_array.zone_array _zones 
	cdef _migration.mig_specs _migration 

