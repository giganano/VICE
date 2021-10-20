# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from .....core.objects._multizone cimport MULTIZONE
from ._generic cimport generic

cdef class no_migration(generic):
	pass


### No migration edge case unit tests ###
cdef extern from "../agb.h":
	unsigned short no_migration_test_m_AGB_from_tracers(MULTIZONE *mz)

cdef extern from "../ism.h":
	unsigned short no_migration_test_multizone_unretained(MULTIZONE *mz)

cdef extern from "../migration.h":
	unsigned short no_migration_test_migrate(MULTIZONE *mz)

cdef extern from "../multizone.h":
	unsigned short no_migration_test_multizone_stellar_mass(MULTIZONE *mz)

cdef extern from "../recycling.h":
	unsigned short no_migration_test_recycle_metals_from_tracers(MULTIZONE *mz)
	unsigned short no_migration_test_gas_recycled_in_zones(MULTIZONE *mz)

cdef extern from "../sneia.h":
	unsigned short no_migration_test_m_sneia_from_tracers(MULTIZONE *mz)
