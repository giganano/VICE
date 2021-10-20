# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
from ._callback_1arg cimport CALLBACK_1ARG


cdef extern from "../../src/objects.h":
	ctypedef struct IMF_:
		char *spec
		double m_lower
		double m_upper
		CALLBACK_1ARG *custom_imf


cdef extern from "../../src/imf.h":
	IMF_ *imf_initialize(double m_lower, double m_upper)
	void imf_free(IMF_ *imf)


cdef IMF_ *imf_object(user_spec, m_lower, m_upper) except *

