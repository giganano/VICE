# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test",
	"test_euler",
	"test_trapezoid",
	"test_midpoint",
	"test_simpson"
]
from ...testing import moduletest
from ...testing import unittest
from . cimport _integral


@moduletest
def test():
	"""
	Tests this module
	"""
	return ["vice.src.yields.integral",
		[
			test_euler(),
			test_trapezoid(),
			test_midpoint(),
			test_simpson()
		]
	]


@unittest
def test_euler():
	"""
	Tests the euler's method integration routine at vice/src/yields/integral.c
	"""
	return ["vice.src.yields.integral [method :: euler]",
		_integral.test_quad_euler]


@unittest
def test_trapezoid():
	"""
	Tests the trapezoid rule integration routine at vice/src/yields/integral.c
	"""
	return ["vice.src.yields.integral [method :: trapezoid]",
		_integral.test_quad_trapzd]


@unittest
def test_midpoint():
	"""
	Tests the midpoint rule integration routine at vice/src/yields/integral.c
	"""
	return ["vice.src.yields.integral [method :: midpoint]",
		_integral.test_quad_midpt]


@unittest
def test_simpson():
	"""
	Tests the Simpson's rule integration routine at vice/src/yields/integral.c
	"""
	return ["vice.src.yields.integral [method :: simpson]",
		_integral.test_quad_simp]

