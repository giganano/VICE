# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from .....core.objects._multizone cimport MULTIZONE
from ._generic cimport generic


cdef class separation(generic):
	pass


### Separation edge case unit tests ###
cdef extern from "../agb.h":
	unsigned short separation_test_m_AGB_from_tracers(MULTIZONE *mz)

cdef extern from "../element.h":
	unsigned short separation_test_update_elements(MULTIZONE *mz)

cdef extern from "../ism.h":
	unsigned short separation_test_update_zone_evolution(MULTIZONE *mz)

cdef extern from "../mdf.h":
	unsigned short separation_test_tracers_MDF(MULTIZONE *mz)

cdef extern from "../migration.h":
	unsigned short separation_test_migrate(MULTIZONE *mz)

cdef extern from "../multizone.h":
	unsigned short separation_test_multizone_stellar_mass(MULTIZONE *mz)

cdef extern from "../recycling.h":
	unsigned short separation_test_recycle_metals_from_tracers(MULTIZONE *mz)
	unsigned short separation_test_gas_recycled_in_zones(MULTIZONE *mz)

cdef extern from "../sneia.h":
	unsigned short separation_test_m_sneia_from_tracers(MULTIZONE *mz)

