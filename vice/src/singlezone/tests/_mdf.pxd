# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....core.objects._singlezone cimport SINGLEZONE

cdef extern from "../mdf.h":
	unsigned short setup_MDF(SINGLEZONE *sz)
