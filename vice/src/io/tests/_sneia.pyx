# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test",
	"test_ia_yield_lookup"
]
from ....testing import moduletest
from ....testing import unittest
from . cimport _sneia


@moduletest
def test():
	"""
	Run the tests on this module
	"""
	return ["vice.src.io.sneia",
		[
			test_ia_yield_lookup()
		]
	]


@unittest
def test_ia_yield_lookup():
	"""
	Test the SN Ia mass yield lookup function at vice/src/io/sneia.h
	"""
	return ["vice.src.io.sneia.single_ia_mass_yield_lookup",
		_sneia.test_single_ia_mass_yield_lookup]

