# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_sneia_yield_specs_constructor", 
	"test_sneia_yield_specs_destructor" 
] 
from .._test_utils import unittest 
from . cimport _sneia 


def test_sneia_yield_specs_constructor(): 
	""" 
	Tests the SNe Ia yield specs constructor function at 
	vice/src/objects/sneia.h 
	""" 
	return unittest("SN Ia yield specifications constructor", 
		_sneia.test_sneia_yield_initialize) 


def test_sneia_yield_specs_destructor(): 
	""" 
	Tests the SNe Ia yield specs destructor function at 
	vice/src/objects/sneia.h 
	""" 
	return unittest("SN Ia yield specifications destructor", 
		_sneia.test_sneia_yield_free) 

