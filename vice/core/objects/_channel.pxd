# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._element cimport ELEMENT
from ._callback_1arg cimport CALLBACK_1ARG

cdef extern from "../../src/objects.h":
	ctypedef struct CHANNEL:
		CALLBACK_1ARG *yield_
		double *rate
		double entrainment

cdef extern from "../../src/channel.h":
	CHANNEL *channel_initialize()
	void channel_free(CHANNEL *ch)
	void normalize_rates(ELEMENT *e, unsigned long length)

