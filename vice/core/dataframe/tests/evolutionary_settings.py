"""
Test the evolutionary settings derived class
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from .._evolutionary_settings import evolutionary_settings
from ....testing import moduletest
from ....testing import unittest


@moduletest
def test():
	"""
	Run all tests on the evolutionary_settings derived class
	"""
	return ["vice.core.dataframe.evolutionary_settings",
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
		Tests the initialization of the evolutionary_settings derived class
		"""
		global _TEST_FRAME_
		_TEST_FRAME_ = dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [0.]
		))
		try:
			_TEST_FRAME_ = evolutionary_settings(_TEST_FRAME_, "test")
		except:
			return False
		return isinstance(_TEST_FRAME_, evolutionary_settings)
	return ["vice.core.dataframe.evolutionary_settings.__init__", test]


@unittest
def test_setitem():
	"""
	__setitem__ unit test
	"""
	def test():
		"""
		Tests the setitem function
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				_TEST_FRAME_[i] = 0.5
		except:
			return False
		if _TEST_FRAME_ == evolutionary_settings(dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [0.5]
		)), "test"):
			try:
				for i in _RECOGNIZED_ELEMENTS_:
					_TEST_FRAME_[i] = dummy
			except:
				return False
		else:
			return False
		return _TEST_FRAME_ == evolutionary_settings(dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [dummy]
		)), "test")
	return ["vice.core.dataframe.evolutionary_settings.__setitem__", test]


def dummy(t):
	"""
	A dummy function of time
	"""
	return t**2

