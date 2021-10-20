# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_ssp_constructor",
	"test_ssp_destructor"
]
from ....testing import unittest
from . cimport _ssp


@unittest
def test_ssp_constructor():
	"""
	Tests the SSP constructor function at vice/src/objects/ssp.h
	"""
	return ["vice.src.objects.ssp constructor", _ssp.test_ssp_initialize]


@unittest
def test_ssp_destructor():
	"""
	Tests the SSP destructor function at vice/src/objects/ssp.h
	"""
	return ["vice.src.objects.ssp destructor", _ssp.test_ssp_free]

