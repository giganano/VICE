# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._noncustomizable cimport noncustomizable

cdef class saved_yields(noncustomizable):
	pass

