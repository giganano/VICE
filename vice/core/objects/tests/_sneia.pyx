# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_sneia_yield_specs_constructor",
	"test_sneia_yield_specs_destructor"
]
from ....testing import unittest
from . cimport _sneia


@unittest
def test_sneia_yield_specs_constructor():
	"""
	Tests the SNe Ia yield specs constructor function at
	vice/src/objects/sneia.h
	"""
	return ["vice.src.objects.sneia_yield_specs constructor",
		_sneia.test_sneia_yield_initialize]


@unittest
def test_sneia_yield_specs_destructor():
	"""
	Tests the SNe Ia yield specs destructor function at
	vice/src/objects/sneia.h
	"""
	return ["vice.src.objects.sneia_yield_specs destructor",
		_sneia.test_sneia_yield_free]

