# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..dataframe._fromfile cimport fromfile
from ..dataframe._base cimport base

cdef class c_multioutput:
	cdef base _zones
	cdef fromfile _stars
	cdef object _name

