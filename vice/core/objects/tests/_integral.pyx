# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_integral_constructor",
	"test_integral_destructor"
]
from ....testing import unittest
from . cimport _integral


@unittest
def test_integral_constructor():
	"""
	Tests the integral constructor function at vice/src/objects/integral.h
	"""
	return ["vice.src.objects.integral constructor",
		_integral.test_integral_initialize]


@unittest
def test_integral_destructor():
	"""
	Tests the integral destructor function at vice/src/objects/integral.h
	"""
	return ["vice.src.objects.integral destructor",
		_integral.test_integral_free]

