# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from . cimport _agb 
from . cimport _ccsne 
from . cimport _sneia 
from . cimport _channel 

cdef extern from "../../src/objects.h": 
	ctypedef struct ELEMENT: 
		_agb.AGB_YIELD_GRID *agb_grid 
		_ccsne.CCSNE_YIELD_SPECS *ccsne_yields 
		_sneia.SNEIA_YIELD_SPECS *sneia_yields 
		_channel.CHANNEL **channels 
		unsigned short n_channels 
		char *symbol 
		double *Z 
		double *Zin 
		double primordial 
		double mass 
		double solar 

cdef extern from "../../src/element.h": 
	ELEMENT *element_initialize() 
	void element_free(ELEMENT *e) 

