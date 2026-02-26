r"""
This file implements testing of the elements.py file in the parent directory.
"""

from __future__ import absolute_import
__all__ = ["test"]
from .._globals import _RECOGNIZED_ELEMENTS_
from .._globals import _VERSION_ERROR_
from ..testing import moduletest
from ..testing import unittest
from .. import elements
import numbers
import sys
import os
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


@moduletest
def test():
	r"""
	vice.elements moduletest
	"""
	return ["vice.elements",
		[
			test_element(),
			test_destroyed_by_stars(),
			test_nonmetals(),
			test_yields()
		]
	]


@unittest
def test_element():
	r"""
	vice.elements.element unittest
	"""
	def test():
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				test = elements.element(i)
				assert test.symbol.lower() == i.lower()
				assert isinstance(test.name, strcomp) and len(test.name) > 2
				assert isinstance(test.yields, elements.yields)
				assert isinstance(test.atomic_number, int)
				assert isinstance(test.primordial, numbers.Number)
				assert 0 <= test.primordial < 1
				assert isinstance(test.solar_z, float)
				assert 0 <= test.solar_z < 1
				assert isinstance(test.sources, list)
				assert all(map(lambda x: isinstance(x, strcomp), test.sources))
				assert isinstance(test.stable_isotopes, list)
				assert all(map(lambda x: isinstance(x, int),
					test.stable_isotopes))
		except:
			return False
		return True
	return ["vice.elements.element", test]


@unittest
def test_destroyed_by_stars():
	r"""
	vice.elements.destroyed_by_stars unittest
	"""
	def test():
		try:
			assert os.environ["VICE_DESTROYED_BY_STARS"] == ""
			assert elements.destroyed_by_stars() == []
			elements.destroyed_by_stars("au")
			assert os.environ["VICE_DESTROYED_BY_STARS"] == "au"
			assert elements.destroyed_by_stars() == ["au"]
			elements.destroyed_by_stars("au", "ag", "ne")
			assert os.environ["VICE_DESTROYED_BY_STARS"] == "au,ag,ne"
			assert elements.destroyed_by_stars() == ["au", "ag", "ne"]
			elements.destroyed_by_stars(None)
			assert os.environ["VICE_DESTROYED_BY_STARS"] == ""
			assert elements.destroyed_by_stars() == []
		except:
			return False
		return True
	return ["vice.elements.destroyed_by_stars", test]


@unittest
def test_nonmetals():
	r"""
	vice.elements.nonmetals unittest
	"""
	def test():
		try:
			assert os.environ["VICE_NONMETALS"] == "he"
			assert elements.nonmetals() == ["he"]
			elements.nonmetals("he", "au", "ne")
			assert os.environ["VICE_NONMETALS"] == "he,au,ne"
			assert elements.nonmetals() == ["he", "au", "ne"]
			elements.nonmetals("he", "au")
			assert os.environ["VICE_NONMETALS"] == "he,au"
			assert elements.nonmetals() == ["he", "au"]
			elements.nonmetals("he")
			assert os.environ["VICE_NONMETALS"] == "he"
			assert elements.nonmetals() == ["he"]
		except:
			return False
		return True
	return ["vice.elements.nonmetals", test]


@unittest
def test_yields():
	r"""
	vice.elements.yields unittest
	"""
	def test():
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				test = elements.yields(i)
				assert isinstance(test.agb, strcomp) or callable(test.agb)
				assert isinstance(test.ccsne, numbers.Number) or callable(
					test.ccsne)
				assert isinstance(test.sneia, numbers.Number) or callable(
					test.sneia)
		except:
			return False
		return True
	return ["vice.elements.yields", test]



