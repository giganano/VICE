# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._base cimport base

cdef class ccsn_yield_table(base):
	cdef object _masses
	cdef object _isotopes
	cdef object _yields

