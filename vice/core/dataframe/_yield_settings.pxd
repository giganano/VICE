# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._elemental_settings cimport elemental_settings

cdef class yield_settings(elemental_settings):
	cdef object __defaults
	cdef object _allow_funcs
	cdef object _config_field
	cdef object _name

