"""
Tests the channel_entrainment derived class
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from .._entrainment import channel_entrainment
from ....testing import moduletest
from ....testing import unittest


@moduletest
def test(run = True):
	"""
	Run all tests on the channel_entrainment derived class
	"""
	return ["vice.core.dataframe.channel_entrainment",
		[
			test_initialization(),
			test_setitem()
		]
	]


@unittest
def test_initialization():
	"""
	Initialization unit test
	"""
	def test():
		"""
		Tests the initialization of the channel_entrainment derived class
		"""
		global _TEST_FRAME_
		_TEST_FRAME_ = dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [1.]
		))
		try:
			_TEST_FRAME_ = channel_entrainment(_TEST_FRAME_)
		except:
			return False
		return isinstance(_TEST_FRAME_, channel_entrainment)
	return ["vice.core.dataframe.channel_entrainment.__init__", test]


@unittest
def test_setitem():
	"""
	__setitem__ unit test
	"""
	def test():
		"""
		Tests the __setitem__ function
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				_TEST_FRAME_[i] = 0.5
		except:
			return False
		return _TEST_FRAME_ == channel_entrainment(dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [0.5]
		)))
	return ["vice.core.dataframe.channel_entrainment.__setitem__", test]

