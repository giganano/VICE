# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._multizone cimport MULTIZONE
from ..objects._multizone cimport multizone_initialize
from ..objects._multizone cimport multizone_evolve
from ..objects._multizone cimport multizone_cancel
from ..objects._multizone cimport multizone_free
from ..objects._multizone cimport link_zone
from . cimport _zone_array
from . cimport _migration


cdef class c_multizone:
	cdef MULTIZONE *_mz
	cdef _zone_array.zone_array _zones
	cdef _migration.mig_specs _migration

