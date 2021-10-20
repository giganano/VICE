# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....core.objects._singlezone cimport SINGLEZONE

cdef extern from "../sneia.h":
	unsigned short setup_RIa(SINGLEZONE *sz)
