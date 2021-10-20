# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_interp_scheme_2d_constructor",
	"test_interp_scheme_2d_destructor"
]
from ....testing import unittest
from . cimport _interp_scheme_2d


@unittest
def test_interp_scheme_2d_constructor():
	r"""
	Tests the interp_scheme_2d constructor at
	vice/src/objects/interp_scheme_2d.h
	"""
	return ["vice.src.objects.interp_scheme_2d constructor",
		_interp_scheme_2d.test_interp_scheme_2d_initialize]


@unittest
def test_interp_scheme_2d_destructor():
	r"""
	Tests the interp_scheme_2d destructor at
	vice/src/objects/interp_scheme_2d.h
	"""
	return ["vice.src.objects.interp_scheme_2d destructor",
		_interp_scheme_2d.test_interp_scheme_2d_free]

