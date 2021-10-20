# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = [
	"test",
	"test_agb_grid_import"
]
from ....testing import moduletest
from ....testing import unittest
from . cimport _agb


@moduletest
def test():
	"""
	Run the tests on this module
	"""
	return ["vice.src.io.agb",
		[
			test_agb_grid_import()
		]
	]


@unittest
def test_agb_grid_import():
	"""
	Tests the AGB star yield grid import function at vice/src/io/agb.h
	"""
	return ["vice.src.io.agb.import_agb_grid", _agb.test_import_agb_grid]

