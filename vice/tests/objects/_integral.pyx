# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_integral_constructor", 
	"test_integral_destructor" 
] 
from . cimport _integral 

_RETURN_VALUE_MESSAGE_ = { 
	1: 		"Success", 
	0: 		"Failure" 
}


def test_integral_constructor(): 
	""" 
	Tests the integral constructor function at vice/src/objects/integral.h 
	""" 
	print("Integral constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_integral.test_integral_initialize()] 
	)) 


def test_integral_destructor(): 
	""" 
	Tests the integral destructor function at vice/src/objects/integral.h 
	""" 
	print("Integral destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_integral.test_integral_free()] 
	)) 

