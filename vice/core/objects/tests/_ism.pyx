# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_ism_constructor",
	"test_ism_destructor"
]
from ....testing import unittest
from . cimport _ism


@unittest
def test_ism_constructor():
	"""
	Tests the ISM constructor function at vice/src/objects/ism.h
	"""
	return ["vice.src.objects.ism constructor", _ism.test_ism_initialize]


@unittest
def test_ism_destructor():
	"""
	Tests the ISM destructor function at vice/src/objects/ism.h
	"""
	return ["vice.src.objects.ism destructor", _ism.test_ism_free]

