
from __future__ import absolute_import
__all__ = ["test"]
from ....testing import moduletest
from ....testing import unittest
from .._fromfile import fromfile
from .._base import base
from ...singlezone import singlezone
import numbers


@moduletest
def test():
	r"""
	vice.core.dataframe.fromfile module test
	"""
	return ["vice.core.dataframe.fromfile",
		[
			test_initialize(),
			test_getitem(),
			test_setitem(),
			test_name(),
			test_size(),
			test_keys(),
			test_todict()
		]
	]


@unittest
def test_initialize():
	r"""
	vice.core.dataframe.fromfile.__init__ unit test
	"""
	def test():
		singlezone.singlezone(name = "test").run(
			[0.01 * i for i in range(1001)], overwrite = True)
		with open("test.vice/mdf.out", 'r') as f:
			keys = [i.lower() for i in f.readline().split()[1:]]
			f.close()
		global _TEST_
		try:
			_TEST_ = fromfile(filename = "test.vice/mdf.out", labels = keys)
		except:
			return False
		return isinstance(_TEST_, fromfile)
	return ["vice.core.dataframe.fromfile.__init__", test]


@unittest
def test_getitem():
	r"""
	vice.core.dataframe.fromfile.__getitem__ unit test
	"""
	def test():
		with open("test.vice/mdf.out", 'r') as f:
			keys = [i.lower() for i in f.readline().split()[1:]]
			f.close()
		try:
			for i in keys:
				assert isinstance(_TEST_[i], list)
			for i in range(_TEST_.size[0]):
				assert isinstance(_TEST_[i], base)
				assert _TEST_[i].keys() == _TEST_.keys()
				assert all(map(lambda x: isinstance(x, numbers.Number),
					[_TEST_[i][j] for j in keys]))
		except:
			return False
		return True
	return ["vice.core.dataframe.fromfile.__getitem__", test]


@unittest
def test_setitem():
	r"""
	vice.core.dataframe.fromfile.__setitem__ unit test
	"""
	def test():
		try:
			_TEST_["test"] = len(_TEST_[_TEST_.keys()[0]]) * [0.]
		except:
			return False
		return "test" in _TEST_.keys()
	return ["vice.core.dataframe.fromfile.__setitem__", test]


@unittest
def test_name():
	r"""
	vice.core.dataframe.fromfile.name unit test
	"""
	def test():
		return _TEST_.name == "test.vice/mdf.out"
	return ["vice.core.dataframe.fromfile.name", test]


@unittest
def test_size():
	r"""
	vice.core.dataframe.fromfile.size unit test
	"""
	def test():
		return (isinstance(_TEST_.size, tuple) and
			len(_TEST_.size) == 2 and
			isinstance(_TEST_.size[0], int) and
			isinstance(_TEST_.size[1], int)
		)
	return ["vice.core.dataframe.fromfile.size", test]


@unittest
def test_keys():
	r"""
	vice.core.dataframe.fromfile.keys unit test
	"""
	def test():
		with open("test.vice/mdf.out", 'r') as f:
			keys = [i.lower() for i in f.readline().split()[1:]]
			f.close()
		keys.append("test") # from the __setitem__ unit test
		try:
			test_ = _TEST_.keys()
		except:
			return False
		return test_ == keys
	return ["vice.core.dataframe.fromfile.keys", test]


@unittest
def test_todict():
	r"""
	vice.core.dataframe.fromfile.todict unit test
	"""
	def test():
		try:
			test_ = _TEST_.todict()
		except:
			return False
		return isinstance(test_, dict)
	return ["vice.core.dataframe.fromfile.todict", test]


