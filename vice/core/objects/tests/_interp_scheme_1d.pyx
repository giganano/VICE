# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test_interp_scheme_1d_constructor",
	"test_interp_scheme_1d_destructor"
]
from ....testing import unittest
from . cimport _interp_scheme_1d


@unittest
def test_interp_scheme_1d_constructor():
	r"""
	Tests the interp_scheme_1d constructor at
	vice/src/objects/interp_scheme_1d.h
	"""
	return ["vice.src.objects.interp_scheme_1d constructor",
		_interp_scheme_1d.test_interp_scheme_1d_initialize]


@unittest
def test_interp_scheme_1d_destructor():
	r"""
	Tests the interp_scheme_1d destructor at
	vice/src/objects/interp_scheme_1d.h
	"""
	return ["vice.src.objects.interp_scheme_1d destructor",
		_interp_scheme_1d.test_interp_scheme_1d_free]

