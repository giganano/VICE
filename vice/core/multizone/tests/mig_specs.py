r"""
This file implements testing of the migration.specs object.
"""

from __future__ import absolute_import
__all__ = ["test"]
from ....testing import moduletest
from ....testing import unittest
from .._migration import mig_specs
from .._migration import mig_matrix
from .mig_matrix import _TEST_SIZE_


@moduletest
def test():
	r"""
	vice.migration.specs module test
	"""
	return ["vice.core.multizone.migration.specs",
		[
			test_initialization(),
			test_gas(),
			test_stars()
		]
	]


@unittest
def test_initialization():
	r"""
	vice.migration.specs.__init__ unit test
	"""
	def test():
		global _TEST_
		try:
			_TEST_ = mig_specs(_TEST_SIZE_)
		except:
			return False
		return isinstance(_TEST_, mig_specs)
	return ["vice.core.multizone.migration.specs.__init__", test]


@unittest
def test_gas():
	r"""
	vice.migration.specs.gas.setter unit test
	"""
	def test():
		try:
			test_matrix = mig_matrix(_TEST_SIZE_)
		except:
			return None
		try:
			_TEST_.gas = test_matrix
		except:
			return False
		return _TEST_.gas == test_matrix
	return ["vice.core.multizone.migration.specs.gas.setter", test]


@unittest
def test_stars():
	r"""
	vice.migration.specs.stars.setter unit test
	"""
	def test():
		def test_stellar_prescription(zone, t1, t2):
			return zone
		try:
			_TEST_.stars = test_stellar_prescription
		except:
			return False
		return _TEST_.stars == test_stellar_prescription
	return ["vice.core.multizone.migration.specs.stars.setter", test]

