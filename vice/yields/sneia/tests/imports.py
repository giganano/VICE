
from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _RECOGNIZED_ELEMENTS_
from ....testing import moduletest
from ....testing import unittest
import sys


@moduletest
def test():
	r"""
	Run the unit tests on sneia import modules
	"""
	return ["vice.yields.sneia.imports",
		[
			test_iwamoto99_import(),
			test_seitenzahl13_import(),
			test_gronow21_import()
		]
	]


@unittest
def test_iwamoto99_import():
	r"""
	from vice.yields.sneia import iwamoto99 unit test
	"""
	def test():

		try:
			from .. import iwamoto99
		except:
			return False
		return True
	return ["vice.yields.sneia.iwamoto99", test]


@unittest
def test_seitenzahl13_import():
	r"""
	from vice.yields.sneia import seitenzahl13 unit test
	"""
	def test():
		try:
			from .. import seitenzahl13
		except:
			return False
		return True
	return ["vice.yields.sneia.seitenzahl13", test]


@unittest
def test_gronow21_import():
	r"""
	from vice.yields.sneia import gronow21 unit test
	"""
	def test():
		try:
			from .. import gronow21
		except:
			return False
		return True
	return ["vice.yields.sneia.gronow21", test]

