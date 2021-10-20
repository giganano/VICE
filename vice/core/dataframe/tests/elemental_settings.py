"""
Test the elemental_settings derived class
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from ....testing import moduletest
from ....testing import unittest
from .._elemental_settings import elemental_settings
from .._base import base


@moduletest
def test():
	"""
	Tests the elemental_settings derived class of the VICE dataframe
	"""
	return ["vice.core.dataframe.elemental_settings",
		[
			test_initialization(),
			test_getitem(),
			test_remove()
		]
	]


@unittest
def test_initialization():
	"""
	Initialization unit test
	"""
	def test():
		"""
		Tests the initialization of the elemental_settings derived class
		"""
		global _TEST_FRAME_
		_TEST_FRAME_ = dict(zip(
			_RECOGNIZED_ELEMENTS_,
			len(_RECOGNIZED_ELEMENTS_) * [list(range(10))]
		))
		try:
			_TEST_FRAME_ = elemental_settings(_TEST_FRAME_)
		except:
			return False
		return isinstance(_TEST_FRAME_, elemental_settings)
	return ["vice.core.dataframe.elemental_settings.__init__", test]


@unittest
def test_getitem():
	"""
	__getitem__ unit test
	"""
	def test():
		"""
		Tests the getitem function
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert _TEST_FRAME_[i] == list(range(10))
		except:
			return False
		return True
	return ["vice.core.dataframe.elemental_settings.__getitem__", test]


@unittest
def test_remove():
	"""
	Remove function unit test
	"""
	def test():
		"""
		Tests the remove function, which should always throw a TypeError
		"""
		try:
			_TEST_FRAME_.remove(_RECOGNIZED_ELEMENTS_[0])
		except TypeError:
			return True
		except:
			return False
		return False
	return ["vice.core.dataframe.elemental_settings.remove", test]

