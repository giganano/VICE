# cython: language_level = 3, boundscheck = False
#
# This file is part of the VICE package.
# Copyright (C) 2019 James W. Johnson (giganano9@gmail.com)
# License: MIT License. See LICENSE in top-level directory
# at https://github.com/giganano/VICE.git.

from __future__ import absolute_import
from ..singlezone cimport _singlezone
from . cimport _migration


cdef extern from "../../src/objects.h":
	ctypedef struct MULTIZONE:
		char *name
		_singlezone.SINGLEZONE **zones
		_migration.MIGRATION *mig
		unsigned short verbose
		unsigned short simple
		unsigned short nthreads
		unsigned short setup_nthreads


cdef extern from "../../src/multizone/multizone.h":
	MULTIZONE *multizone_initialize(unsigned int n)
	void multizone_free(MULTIZONE *mz)
	void link_zone(MULTIZONE *mz, unsigned long address,
		unsigned int zone_index)
	unsigned short multizone_evolve(MULTIZONE *mz)
	void multizone_cancel(MULTIZONE *mz)

