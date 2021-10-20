# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....core.singlezone._singlezone cimport c_singlezone
from ....core.objects._singlezone cimport SINGLEZONE
from ....core.objects._element cimport ELEMENT


cdef extern from "../singlezone.h":
	extern long singlezone_address(SINGLEZONE *sz)
	extern unsigned long n_timesteps(SINGLEZONE sz)
	extern unsigned short singlezone_setup(SINGLEZONE *sz)
	extern unsigned short singlezone_evolve(SINGLEZONE *sz)
	extern void singlezone_cancel(SINGLEZONE *sz)
	extern void singlezone_clean(SINGLEZONE *sz)


cdef extern from "../../singlezone.h":
	unsigned long BUFFER


cdef class singlezone_tester(c_singlezone):
	pass

