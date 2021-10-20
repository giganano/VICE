# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._yield_settings cimport yield_settings

cdef class agb_yield_settings(yield_settings):
	pass


