# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_mdf_constructor", 
	"test_mdf_destructor" 
] 
from .._test_utils import unittest 
from . cimport _mdf 


@unittest 
def test_mdf_constructor(): 
	""" 
	Tests the MDF constructor function at vice/src/objects/mdf.h 
	""" 
	return ["Stellar metallicity distribution function constructor", 
		_mdf.test_mdf_initialize] 


@unittest 
def test_mdf_destructor(): 
	""" 
	Tests the MDF destructor function at vice/src/objects/mdf.h 
	""" 
	return ["Stellar metallicity distribution function destructor", 
		_mdf.test_mdf_free] 

