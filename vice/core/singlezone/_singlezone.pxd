# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from libc.stdio cimport FILE
from ..objects._singlezone cimport SINGLEZONE
from ..objects._element cimport ELEMENT
from ..objects._channel cimport CHANNEL


cdef extern from "../../src/channel.h":
	CHANNEL *channel_initialize()
	void channel_free(CHANNEL *ch)
	void normalize_channel_rates(CHANNEL *ch, unsigned long length)


cdef class c_singlezone:
	cdef SINGLEZONE *_sz
	cdef object _func
	cdef object _channels
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
	cdef object _callback_custom

