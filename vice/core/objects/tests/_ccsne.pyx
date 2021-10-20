# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_ccsne_yield_specs_constructor",
	"test_ccsne_yield_specs_destructor"
]
from ....testing import unittest
from . cimport _ccsne


@unittest
def test_ccsne_yield_specs_constructor():
	"""
	Test the CCSNe yield specs constructor at vice/src/objects/ccsne.h
	"""
	return ["vice.src.objects.ccsne_yield_specs constructor",
		_ccsne.test_ccsne_yield_initialize]


@unittest
def test_ccsne_yield_specs_destructor():
	"""
	Test the CCSNe yield specs destructor at vice/src/objects/ccsne.h
	"""
	return ["vice.src.objects.ccsne_yield_specs destructor",
		_ccsne.test_ccsne_yield_free]

