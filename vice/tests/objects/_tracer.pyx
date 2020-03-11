# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_tracer_constructor", 
	"test_tracer_destructor" 
] 
from .._test_utils import unittest 
from . cimport _tracer 


@unittest 
def test_tracer_constructor(): 
	""" 
	Tests the tracer constructor function at vice/src/objects/tracer.h 
	""" 
	return ["Star particle constructor", _tracer.test_tracer_initialize] 


@unittest 
def test_tracer_destructor(): 
	""" 
	Tests the tracer destructor function at vice/src/objects/tracer.h 
	""" 
	return ["Star particle destructor", _tracer.test_tracer_free] 

