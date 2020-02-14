# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_tracer_constructor", 
	"test_tracer_destructor" 
] 
from .._test_utils import _RETURN_VALUE_MESSAGE_ 
from . cimport _tracer 


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

