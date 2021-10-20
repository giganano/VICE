# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....core.objects._singlezone cimport SINGLEZONE

cdef extern from "../ism.h":
	unsigned short setup_gas_evolution(SINGLEZONE *sz)
	unsigned short update_gas_evolution(SINGLEZONE *sz)
