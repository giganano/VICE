# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_multizone_constructor", 
	"test_multizone_destructor" 
] 
from .._test_utils import unittest 
from . cimport _multizone 


def test_multizone_constructor(): 
	""" 
	Tests the multizone constructor function at vice/src/objects/multizone.h 
	""" 
	return unittest("Multizone constructor", 
		_multizone.test_multizone_initialize) 


def test_multizone_destructor(): 
	""" 
	Tests the multizone destructor function at vice/src/objects/multizone.h 
	""" 
	return unittest("Multizone destructor", _multizone.test_multizone_free) 

