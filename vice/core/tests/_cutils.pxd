# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ..objects._callback_1arg cimport CALLBACK_1ARG
from ..objects._callback_2arg cimport CALLBACK_2ARG
from ..objects._imf cimport IMF_


cdef extern from "../../src/objects/callback_1arg.h":
	CALLBACK_1ARG *callback_1arg_initialize()
	void callback_1arg_free(CALLBACK_1ARG *cb1)


cdef extern from "../../src/objects/callback_2arg.h":
	CALLBACK_2ARG *callback_2arg_initialize()
	void callback_2arg_free(CALLBACK_2ARG *cb2)


cdef extern from "../../src/objects/imf.h":
	IMF_ *imf_initialize(double m_lower, double m_upper)
	void imf_free(IMF_ *imf)

