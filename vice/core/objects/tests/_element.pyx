# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_element_constructor",
	"test_element_destructor"
]
from ....testing import unittest
from . cimport _element


@unittest
def test_element_constructor():
	"""
	Tests the element constructor function at vice/src/objects/element.h
	"""
	return ["vice.src.objects.element constructor",
		_element.test_element_initialize]


@unittest
def test_element_destructor():
	"""
	Tests the element destructor function at vice/src/objects/element.h
	"""
	return ["vice.src.objects.element destructor", _element.test_element_free]

