# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test",
	"test_custom_mass_distribution",
	"test_mass_bin_counter",
	"test_imf_evaluation",
	"test_builtin_salpeter",
	"test_builtin_kroupa"
]
from ...testing import moduletest
from ...testing import unittest
from . cimport _imf


@moduletest
def test():
	"""
	Runs the tests on this module
	"""
	return ["vice.src.imf",
		[
			test_imf_evaluation(),
			test_builtin_salpeter(),
			test_builtin_kroupa()
		]
	]


@unittest
def test_imf_evaluation():
	"""
	Tests the function which evaluates and imf at vice/src/imf.h
	"""
	return ["vice.src.imf.evaluate", _imf.test_imf_evaluate]


@unittest
def test_builtin_salpeter():
	"""
	Tests the built-in Salpeter (1955) IMF at vice/src/imf.h
	"""
	return ["vice.src.imf.salpeter55", _imf.test_salpeter55]


@unittest
def test_builtin_kroupa():
	"""
	Tests the built-in Kroupa (2001) IMF at vice/src/imf.h
	"""
	return ["vice.src.imf.kroupa01", _imf.test_kroupa01]

