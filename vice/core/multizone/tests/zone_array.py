
from __future__ import absolute_import
__all__ = ["test"]
from ....testing import moduletest
from ....testing import unittest
from ...singlezone import singlezone
from .._zone_array import zone_array

_TEST_SIZE_ = 10


@moduletest
def test():
	r"""
	vice.core.multizone.zone_array module test
	"""
	return ["vice.core.multizone.zone_array",
		[
			test_initialization(),
			test_len(),
			test_getitem(),
			test_setitem()
		]
	]


@unittest
def test_initialization():
	r"""
	vice.core.multizone.zone_array.__init__ unit test
	"""
	def test():
		global _TEST_
		try:
			_TEST_ = zone_array(_TEST_SIZE_)
		except:
			return False
		return isinstance(_TEST_, zone_array)
	return ["vice.core.multizone.zone_array.__init__", test]


@unittest
def test_len():
	r"""
	vice.core.multizone.zone_array.__len__ unit test
	"""
	def test():
		return len(_TEST_) == _TEST_SIZE_
	return ["vice.core.multizone.zone_array.__len__", test]


@unittest
def test_getitem():
	r"""
	vice.core.multizone.zone_array.__getitem__ unit test
	"""
	def test():
		try:
			status = True
			for i in range(len(_TEST_)):
				status &= isinstance(_TEST_[i], singlezone)
				status &= _TEST_[i].name == "zone%d" % (i)
		except:
			return False
		return status
	return ["vice.core.multizone.zone_array.__getitem__", test]


@unittest
def test_setitem():
	r"""
	vice.core.multizone.zone_array.__setitem__ unit test
	"""
	def test():
		test_idx = 3
		try:
			test_zone = singlezone(name = "test", dt = 0.02,
				elements = ['c', 'n'])
		except:
			return None
		try:
			_TEST_[test_idx] = test_zone
		except:
			return False
		status = _TEST_[test_idx].name == "test"
		status &= _TEST_[test_idx].dt == 0.02
		status &= _TEST_[test_idx].elements == ('c', 'n')
		return status
	return ["vice.core.multizone.zone_array.__setitem__", test]

