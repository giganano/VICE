
from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _DIRECTORY_
from ....testing import moduletest
from ....testing import unittest
from .._yield_settings import yield_settings
import os

_TEST_DICT_ = {
	"c": 0.1,
	"n": lambda x: 0.1 * x
}

@moduletest
def test():
	r"""
	vice.core.dataframe.yield_settings module test
	"""
	return ["vice.core.dataframe.yield_settings",
		[
			test_initialize(),
			test_setitem(),
			test_restore_defaults(),
			test_factory_settings(),
			test_save_defaults()
		]
	]


@unittest
def test_initialize():
	r"""
	vice.core.dataframe.yield_settings.__init__ unit test
	"""
	def test():
		global _TEST_
		try:
			_TEST_ = yield_settings(_TEST_DICT_, "test", True, "ccsne")
		except:
			return False
		return (isinstance(_TEST_, yield_settings) and
			_TEST_.todict() == _TEST_DICT_)
	return ["vice.core.dataframe.yield_settings.__init__", test]


@unittest
def test_setitem():
	r"""
	vice.core.dataframe.yield_settings.__setitem__ unit test
	"""
	def test():
		try:
			_TEST_["c"] = 0.05
			_TEST_["c"] = lambda x: 0.01 * x
			_TEST_["n"] = 0.01
			_TEST_["n"] = lambda x: 0.02 * x
		except:
			return False
		return True
	return ["vice.core.dataframe.yield_settings.__setitem__", test]


@unittest
def test_restore_defaults():
	r"""
	vice.core.dataframe.yield_settings.restore_defaults unit test
	"""
	def test():
		try:
			_TEST_.restore_defaults()
		except:
			return False
		return _TEST_.todict() == _TEST_DICT_
	return ["vice.core.dataframe.yield_settings.restore_defaults", test]


@unittest
def test_factory_settings():
	r"""
	vice.core.dataframe.yield_settings.factory_settings unit test
	"""
	def test():
		try:
			_TEST_.factory_settings()
		except:
			return False
		return _TEST_.todict() == _TEST_DICT_
	return ["vice.core.dataframe.yield_settings.factory_settings", test]


@unittest
def test_save_defaults():
	r"""
	vice.core.dataframe.yields.settings.save_defaults unit test
	"""
	def test():
		try:
			_TEST_.save_defaults()
		except:
			return True
		status = "settings.config" in os.listdir("%syields/ccsne" % (
			_DIRECTORY_))
		if status: os.system("rm -f %syields/ccsne/settings.config" % (
			_DIRECTORY_))
		return status
	return ["vice.core.dataframe.yield_settings.save_defaults", test]

