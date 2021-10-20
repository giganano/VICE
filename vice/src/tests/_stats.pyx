# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test",
	"test_gaussian_sampler",
	"test_conversion_to_pdf"
]
from ...testing import moduletest
from ...testing import unittest
from . cimport _stats


@moduletest
def test():
	"""
	Run all tests in this module
	"""
	return ["vice.src.stats",
		[
			test_conversion_to_pdf(),
		]
	]


@unittest
def test_conversion_to_pdf():
	"""
	Test the conversion to PDF function at vice/src/stats.h
	"""
	return ["vice.src.stats.convert_to_PDF", _stats.test_convert_to_PDF]

