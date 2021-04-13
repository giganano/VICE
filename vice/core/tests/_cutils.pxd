# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
from ..objects._callback_1arg cimport CALLBACK_1ARG 
from ..objects._callback_2arg cimport CALLBACK_2ARG 
from ..objects._imf cimport IMF_ 
from .._cutils cimport callback_1arg_initialize 
from .._cutils cimport callback_1arg_free 
from .._cutils cimport callback_2arg_initialize 
from .._cutils cimport callback_2arg_free 


cdef extern from "../../src/objects/imf.h": 
	IMF_ *imf_initialize(double m_lower, double m_upper) 
	void imf_free(IMF_ *imf) 

