"""
Tests the noncustomizable derived class
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from .._noncustomizable import noncustomizable
from ....testing import moduletest
from ....testing import unittest


@moduletest
def test():
	"""
	Run all tests on the noncustomizable derived class
	"""
	return ["vice.core.dataframe.noncustomizable",
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
		Tests the initialization of the noncustomizable derived class
		"""
		global _TEST_FRAME_
		_TEST_FRAME_ = dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [1.]
		))
		try:
			_TEST_FRAME_ = noncustomizable(_TEST_FRAME_, "test")
		except:
			return False
		return isinstance(_TEST_FRAME_, noncustomizable)
	return ["vice.core.dataframe.noncustomizable.__init__", test]


@unittest
def test_setitem():
	"""
	__setitem__ unit test
	"""
	def test():
		"""
		Test the setitem function, which should always throw a TypeError
		"""
		try:
			_TEST_FRAME_[_RECOGNIZED_ELEMENTS_[0]] = 0.5
		except TypeError:
			return True
		except:
			return False
		return False
	return ["vice.core.dataframe.noncustomizable.__setitem__", test]

