# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ssp_constructor", 
	"test_ssp_destructor" 
] 
from .._test_utils import unittest 
from . cimport _ssp 


def test_ssp_constructor(): 
	""" 
	Tests the SSP constructor function at vice/src/objects/ssp.h 
	""" 
	return unittest("Single stellar population constructor", 
		_ssp.test_ssp_initialize) 


def test_ssp_destructor(): 
	""" 
	Tests the SSP destructor function at vice/src/objects/ssp.h 
	""" 
	return unittest("Single stellar population destructor", 
		_ssp.test_ssp_free) 

