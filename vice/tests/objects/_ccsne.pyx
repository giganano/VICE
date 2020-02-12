# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_ccsne_yield_specs_constructor", 
	"test_ccsne_yield_specs_destructor" 
] 
from . cimport _ccsne 

_RETURN_VALUE_MESSAGE_ = {
	1: 		"Success", 
	0: 		"Failure" 
} 


def test_ccsne_yield_specs_constructor(): 
	""" 
	Test the CCSNe yield specs constructor at vice/src/objects/ccsne.h 
	""" 
	print("CCSNe yield specs constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_ccsne.test_ccsne_yield_initialize()] 
	)) 


def test_ccsne_yield_specs_destructor(): 
	""" 
	Test the CCSNe yield specs destructor at vice/src/objects/ccsne.h 
	""" 
	print("CCSNe yield specs destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_ccsne.test_ccsne_yield_free()] 
	)) 

