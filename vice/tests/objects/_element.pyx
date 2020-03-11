# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_element_constructor", 
	"test_element_destructor" 
] 
from .._test_utils import unittest 
from . cimport _element 


@unittest 
def test_element_constructor(): 
	""" 
	Tests the element constructor function at vice/src/objects/element.h 
	""" 
	return ["Element constructor", _element.test_element_initialize]  


@unittest 
def test_element_destructor(): 
	""" 
	Tests the element destructor function at vice/src/objects/element.h 
	""" 
	return ["Element destructor", _element.test_element_free] 

