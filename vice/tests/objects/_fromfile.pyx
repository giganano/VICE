# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_fromfile_constructor", 
	"test_fromfile_destructor" 
] 
from . cimport _fromfile 

_RETURN_VALUE_MESSAGE_ = { 
	1: 		"Success", 
	0: 		"Failure" 
}


def test_fromfile_constructor(): 
	""" 
	Tests the fromfile constructor function at vice/src/objects/fromfile.h 
	""" 
	print("Fromfile constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_fromfile.test_fromfile_initialize()] 
	)) 


def test_fromfile_destructor(): 
	""" 
	Tests the fromfile destructor function at vice/src/objects/fromfile.h 
	""" 
	print("Fromfile destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_fromfile.test_fromfile_free()]
	)) 

