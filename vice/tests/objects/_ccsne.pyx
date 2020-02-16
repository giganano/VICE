# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ccsne_yield_specs_constructor", 
	"test_ccsne_yield_specs_destructor" 
] 
from .._test_utils import unittest 
from . cimport _ccsne 


def test_ccsne_yield_specs_constructor(): 
	""" 
	Test the CCSNe yield specs constructor at vice/src/objects/ccsne.h 
	""" 
	return unittest("CCSN yield specification constructor", 
		_ccsne.test_ccsne_yield_initialize) 


def test_ccsne_yield_specs_destructor(): 
	""" 
	Test the CCSNe yield specs destructor at vice/src/objects/ccsne.h 
	""" 
	return unittest("CCSN yield specification destructor", 
		_ccsne.test_ccsne_yield_free) 

