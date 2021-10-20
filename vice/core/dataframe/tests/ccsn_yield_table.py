
from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _VERSION_ERROR_
from ....testing import moduletest
from ....testing import unittest
from .._ccsn_yield_table import ccsn_yield_table
from .._base import base
import numbers
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


@moduletest
def test():
	r"""
	vice.core.dataframe.ccsn_yield_table module test
	"""
	return ["vice.core.dataframe.ccsn_yield_table",
		[
			test_initialization(),
			test_getitem(),
			test_masses(),
			test_isotopes(),
			test_keys(),
			test_todict()
		]
	]


@unittest
def test_initialization():
	r"""
	vice.core.dataframe.ccsn_yield_table.__init__ unit test
	"""
	def test():
		global _TEST_NONISOTOPIC_
		global _TEST_ISOTOPIC_
		try:
			_TEST_NONISOTOPIC_ = ccsn_yield_table([1, 2, 3], [4, 5, 6])
			_TEST_ISOTOPIC_ = ccsn_yield_table([1, 2],
				((1, 1), (2, 2)), isotopes = ['1', '2'])
		except:
			return False
		return (isinstance(_TEST_NONISOTOPIC_, ccsn_yield_table) and
			isinstance(_TEST_ISOTOPIC_, ccsn_yield_table))
	return ["vice.core.dataframe.ccsn_yield_table.__init__", test]


@unittest
def test_getitem():
	r"""
	vice.core.dataframe.ccsn_yield_table.__getitem__ unit test
	"""
	def test():
		try:
			for i in [1, 2, 3]:
				assert isinstance(_TEST_NONISOTOPIC_[i], numbers.Number)
			for i in [1, 2]:
				assert isinstance(_TEST_ISOTOPIC_[i], base)
				assert isinstance(_TEST_ISOTOPIC_[str(i)], base)
		except:
			return False
		return True
	return ["vice.core.dataframe.ccsn_yield_table.__getitem__", test]


@unittest
def test_masses():
	r"""
	vice.core.dataframe.ccsn_yield_table.masses unit test
	"""
	def test():
		return (
			isinstance(_TEST_NONISOTOPIC_.masses, tuple) and
			all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_NONISOTOPIC_.masses)),
			isinstance(_TEST_ISOTOPIC_.masses, tuple) and
			all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_ISOTOPIC_.masses))
		)
	return ["vice.core.dataframe.ccsn_yield_table.masses", test]


@unittest
def test_isotopes():
	r"""
	vice.core.dataframe.ccsn_yield_table.isotopes unit test
	"""
	def test():
		return (
			isinstance(_TEST_ISOTOPIC_.isotopes, tuple) and
			all(map(lambda x: isinstance(x, strcomp),
				_TEST_ISOTOPIC_.isotopes)) and
			_TEST_NONISOTOPIC_.isotopes is None
		)
	return ["vice.core.dataframe.ccsn_yield_table.isotopes", test]


@unittest
def test_keys():
	r"""
	vice.core.dataframe.ccsn_yield_table.keys unit test
	"""
	def test():
		return (_TEST_ISOTOPIC_.keys() == list(_TEST_ISOTOPIC_.isotopes) and
			_TEST_NONISOTOPIC_.keys() == list(_TEST_NONISOTOPIC_.masses)
		)
	return ["vice.core.dataframe.ccsn_yield_table.keys", test]


@unittest
def test_todict():
	r"""
	vice.core.dataframe.ccsn_yield_table.todict unit test
	"""
	def test():
		return (isinstance(_TEST_NONISOTOPIC_.todict(), dict) and
			isinstance(_TEST_ISOTOPIC_.todict(), dict))
	return ["vice.core.dataframe.ccsn_yield_table.todict", test]

