# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ...objects._multizone cimport MULTIZONE
from .._multizone cimport c_multizone

cdef class multizone_tester(c_multizone):
	pass
