# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._elemental_settings cimport elemental_settings

cdef class noncustomizable(elemental_settings):
	cdef object _name

