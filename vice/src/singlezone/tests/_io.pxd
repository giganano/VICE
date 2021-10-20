# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....core.objects._singlezone cimport SINGLEZONE

cdef extern from "../../io/singlezone.h":
	unsigned short singlezone_open_files(SINGLEZONE *sz)
	void singlezone_close_files(SINGLEZONE *sz)

