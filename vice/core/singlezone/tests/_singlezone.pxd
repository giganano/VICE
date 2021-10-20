# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ...objects._singlezone cimport SINGLEZONE
from ...objects._element cimport ELEMENT
from .._singlezone cimport c_singlezone


cdef class singlezone_tester(c_singlezone):
	pass

