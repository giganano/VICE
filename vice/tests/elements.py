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



