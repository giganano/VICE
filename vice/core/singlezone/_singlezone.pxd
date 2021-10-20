# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from libc.stdio cimport FILE
from ..objects._singlezone cimport SINGLEZONE


cdef class c_singlezone:
	cdef SINGLEZONE *_sz
	cdef object _func
	cdef object _imf
	cdef object _eta
	cdef object _enhancement
	cdef object _entrainment
	cdef object _tau_star
	cdef object _zin
	cdef object _ria
	cdef double _Mg0
	cdef object _agb_model
	cdef object _callback_cc
	cdef object _callback_ia
	cdef object _callback_agb

