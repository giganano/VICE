# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_singlezone_constructor", 
	"test_singlezone_destructor" 
]
from . cimport _singlezone 

_RETURN_VALUE_MESSAGE_ = {
	1: 		"Success", 
	0: 		"Failure" 
}


def test_singlezone_constructor(): 
	""" 
	Tests the singlezone constructor function at vice/src/objects/singlezone.h 
	""" 
	print("Singlezone constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_singlezone.test_singlezone_initialize()] 
	)) 


def test_singlezone_destructor(): 
	""" 
	Tests the singlezone destructor function at vice/src/objects/singlezone.h 
	""" 
	print("Singlezone destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_singlezone.test_singlezone_free()]
	)) 

