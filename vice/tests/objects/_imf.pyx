# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_imf_constructor", 
	"test_imf_destructor" 
] 
from .._test_utils import unittest 
from . cimport _imf 


@unittest 
def test_imf_constructor(): 
	""" 
	Tests the IMF constructor function at vice/src/objects/imf.h 
	""" 
	return ["Stellar IMF constructor", _imf.test_imf_initialize] 


@unittest 
def test_imf_destructor(): 
	""" 
	Tests the IMF destructor function at vice/src/objects/imf.h 
	""" 
	return ["Stellar IMF destructor", _imf.test_imf_free] 

