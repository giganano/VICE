# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from libc.stdio cimport FILE
from . cimport _tracer
from . cimport _multizone


cdef extern from "../../src/objects.h":
	ctypedef struct MIGRATION:
		unsigned int n_zones
		unsigned int n_tracers
		unsigned long tracer_count
		double ***gas_migration
		_tracer.TRACER **tracers
		FILE *tracers_output


cdef extern from "../../src/objects/migration.h":
	MIGRATION *migration_initialize(unsigned int n)
	void migration_free(MIGRATION *mig)

