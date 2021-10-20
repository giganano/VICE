# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ....core.objects._element cimport ELEMENT

cdef extern from "../element.h":
	unsigned short malloc_Z(ELEMENT *e, unsigned long n_timesteps)

