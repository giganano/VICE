# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ism_constructor", 
	"test_ism_destructor" 
] 
from .._test_utils import unittest 
from . cimport _ism 


@unittest 
def test_ism_constructor(): 
	""" 
	Tests the ISM constructor function at vice/src/objects/ism.h 
	""" 
	return ["Interstellar medium constructor", _ism.test_ism_initialize] 


@unittest 
def test_ism_destructor(): 
	""" 
	Tests the ISM destructor function at vice/src/objects/ism.h 
	""" 
	return ["Interstellar medium destructor", _ism.test_ism_free] 

