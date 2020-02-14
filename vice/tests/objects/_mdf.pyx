# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_mdf_constructor", 
	"test_mdf_destructor" 
] 
from .._test_utils import _RETURN_VALUE_MESSAGE_ 
from . cimport _mdf 


def test_mdf_constructor(): 
	""" 
	Tests the MDF constructor function at vice/src/objects/mdf.h 
	""" 
	print("MDF constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_mdf.test_mdf_initialize()] 
	)) 


def test_mdf_destructor(): 
	""" 
	Tests the MDF destructor function at vice/src/objects/mdf.h 
	""" 
	print("MDF destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_mdf.test_mdf_free()] 
	)) 

