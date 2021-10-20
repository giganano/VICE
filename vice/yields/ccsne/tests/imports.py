r"""
Tests the yield imports for CCSN yields
"""

from __future__ import absolute_import
__all__ = [
	"test"
]
from ....testing import moduletest
from ....testing import unittest


@moduletest
def test():
	r"""
	Test the yield import functions
	"""
	return ["vice.yields.ccsne.import",
		[
			test_LC18_import(),
			test_S16_import(),
			test_S16_N20_import(),
			test_S16_W18_import(),
			test_S16_W18F_import(),
			test_NKT13_import(),
			test_CL13_import(),
			test_CL04_import(),
			test_WW95_import(),
		]
	]


@unittest
def test_LC18_import():
	r"""
	from vice.yields.ccsne import LC18 unit test
	"""
	def test():
		try:
			from .. import LC18
		except:
			return False
		return True
	return ["vice.yields.ccsne.LC18", test]


@unittest
def test_S16_import():
	r"""
	from vice.yields.ccsne import S16 unittest
	"""
	def test():
		try:
			from .. import S16
		except:
			return False
		return True
	return ["vice.yields.ccsne.S16", test]


@unittest
def test_S16_N20_import():
	r"""
	from vice.yields.ccsne.S16 import N20 unittest
	"""
	def test():
		try:
			from ..S16 import N20
		except:
			return False
		return True
	return ["vice.yields.ccsne.S16.N20", test]


@unittest
def test_S16_W18_import():
	r"""
	from vice.yields.ccsne.S16 import W18 unittest
	"""
	def test():
		try:
			from ..S16 import W18
		except:
			return False
		return True
	return ["vice.yields.ccsne.S16.W18", test]


@unittest
def test_S16_W18F_import():
	r"""
	from vice.yields.ccsne.S16 import W18F unittest
	"""
	def test():
		try:
			from ..S16 import W18F
		except:
			return False
		return True
	return ["vice.yields.ccsne.S16.W18F", test]


@unittest
def test_NKT13_import():
	r"""
	from vice.yields.ccsne import NKT13 unit test
	"""
	def test():
		try:
			from .. import NKT13
		except:
			return False
		return True
	return ["vice.yields.ccsne.NKT13", test]


@unittest
def test_CL13_import():
	r"""
	from vice.yields.ccsne import CL13 unit test
	"""
	def test():
		try:
			from .. import CL13
		except:
			return False
		return True
	return ["vice.yields.ccsne.CL13", test]


@unittest
def test_CL04_import():
	r"""
	from vice.yields.ccsne import CL04 unit test
	"""
	def test():
		try:
			from .. import CL04
		except:
			return False
		return True
	return ["vice.yields.ccsne.CL04", test]


@unittest
def test_WW95_import():
	r"""
	from vice.yields.ccsne import WW95 unit test
	"""
	def test():
		try:
			from .. import WW95
		except:
			return False
		return True
	return ["vice.yields.ccsne.WW95", test]

