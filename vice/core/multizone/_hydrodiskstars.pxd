# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._multizone cimport MULTIZONE
from ..objects._hydrodiskstars cimport HYDRODISKSTARS
from ..objects._tracer cimport TRACER


cdef extern from "../../src/multizone/hydrodiskstars.h":
	void set_hydrodiskstars_object(unsigned long address)
	unsigned short setup_hydrodisk_tracer(MULTIZONE mz, TRACER *t,
		unsigned int birth_zone, unsigned long birth_timestep,
		long analog_index)

