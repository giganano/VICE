# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._agb cimport AGB_YIELD_GRID
from ._ccsne cimport CCSNE_YIELD_SPECS
from ._sneia cimport SNEIA_YIELD_SPECS
from ._channel cimport CHANNEL
from . cimport _agb
from . cimport _ccsne
from . cimport _sneia
from . cimport _channel

cdef extern from "../../src/objects.h":
	ctypedef struct ELEMENT:
		AGB_YIELD_GRID *agb_grid
		CCSNE_YIELD_SPECS *ccsne_yields
		SNEIA_YIELD_SPECS *sneia_yields
		CHANNEL **channels
		unsigned short n_channels
		char *symbol
		double *Z
		double *Zin
		double primordial
		double unretained
		double mass
		double solar

cdef extern from "../../src/objects/element.h":
	ELEMENT *element_initialize()
	void element_free(ELEMENT *e)

