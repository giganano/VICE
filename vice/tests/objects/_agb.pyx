# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_agb_grid_constructor", 
	"test_agb_grid_destructor" 
] 
from . cimport _agb 

_RETURN_VALUE_MESSAGE_ = {
	1: 		"Success", 
	0: 		"Failure" 
}


def test_agb_grid_constructor(): 
	""" 
	Tests the AGB yield grid constructor function at vice/src/objects/agb.h 
	""" 
	print("AGB yield grid constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_agb.test_agb_yield_grid_initialize()] 
	)) 


def test_agb_grid_destructor(): 
	""" 
	Tests the AGB yield grid destructor function at vice/src/objects/agb.h 
	""" 
	print("AGB yield grid destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_agb.test_agb_yield_grid_free()] 
	)) 

