# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_tracer_constructor", 
	"test_tracer_destructor" 
] 
from . cimport _tracer 

_RETURN_VALUE_MESSAGE_ = { 
	1: 		"Success", 
	0: 		"Failure" 
}


def test_tracer_constructor(): 
	""" 
	Tests the tracer constructor function at vice/src/objects/tracer.h 
	""" 
	print("Tracer constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_tracer.test_tracer_initialize()] 
	)) 


def test_tracer_destructor(): 
	""" 
	Tests the tracer destructor function at vice/src/objects/tracer.h 
	""" 
	print("Tracer destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_tracer.test_tracer_free()] 
	)) 

