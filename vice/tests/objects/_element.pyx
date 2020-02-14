# cython: language_level = 3, boundscheck = False 

from __future__ import absolute_import 
__all__ = [
	"test_element_constructor", 
	"test_element_destructor" 
] 
from .._test_utils import _RETURN_VALUE_MESSAGE_ 
from . cimport _element 


def test_element_constructor(): 
	""" 
	Tests the element constructor function at vice/src/objects/element.h 
	""" 
	print("Element constructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_element.test_element_initialize()]
	)) 


def test_element_destructor(): 
	""" 
	Tests the element destructor function at vice/src/objects/element.h 
	""" 
	print("Element destructor: %s" % (
		_RETURN_VALUE_MESSAGE_[_element.test_element_free()] 
	)) 

