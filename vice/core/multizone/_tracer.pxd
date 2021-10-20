# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._multizone cimport MULTIZONE
from ..objects._tracer cimport TRACER


cdef extern from "../../src/multizone/tracer.h":
	void malloc_tracers(MULTIZONE *mz)


