
from __future__ import absolute_import
__all__ = ["test"]
from ....testing import moduletest
from ....testing import unittest
from .._agb_yield_settings import agb_yield_settings

_TEST_DICT_ = {
	"c": 	"cristallo11",
	"n": 	"karakas10"
}


@moduletest
def test():
	r"""
	vice.core.dataframe.agb_yield_settings module test
	"""
	return ["vice.core.dataframe.agb_yield_settings",
		[
			test_initialize(),
			test_setitem()
		]
	]


@unittest
def test_initialize():
	r"""
	vice.core.dataframe.agb_yield_settings.__init__ unit test
	"""
	def test():
		global _TEST_
		try:
			_TEST_ = agb_yield_settings(_TEST_DICT_, "test", True, "agb")
		except:
			return False
		return (isinstance(_TEST_, agb_yield_settings) and
			_TEST_.todict() == _TEST_DICT_)
	return ["vice.core.dataframe.agb_yield_settings.__init__", test]


@unittest
def test_setitem():
	r"""
	vice.core.dataframe.agb_yield_settings.__setitem__ unit test
	"""
	def test():
		try:
			_TEST_['c'] = "karakas10"
			_TEST_['c'] = lambda m, z: m * z
			_TEST_['n'] = "cristallo11"
			_TEST_['n'] = lambda m, z: 0.1 * m * z
		except:
			return False
		return True
	return ["vice.core.dataframe.agb_yield_settings.__setitem__", test]

