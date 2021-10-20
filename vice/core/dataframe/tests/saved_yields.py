"""
Tests the saved_yields derived class
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from .._saved_yields import saved_yields
from ....testing import moduletest
from ....testing import unittest


@moduletest
def test(run = True):
	"""
	Run all tests on the saved_yields dataframe
	"""
	return ["vice.core.dataframe.saved_yields",
		[
			test_initialization()
		]
	]


@unittest
def test_initialization():
	"""
	Initialization unit test
	"""
	def test():
		"""
		Tests the initialization of the dataframe
		"""
		# Designed to allow numbers, strings, and functions
		global _TEST_FRAME_
		_TEST_FRAME_ = {
			"c": 	1.e-3,
			"n": 	"test",
			"o": 	lambda x: 0.1 * x
		}
		try:
			_TEST_FRAME_ = saved_yields(_TEST_FRAME_, "test")
		except:
			return False
		return isinstance(_TEST_FRAME_, saved_yields)
	return ["vice.core.dataframe.saved_yields.__init__", test]

