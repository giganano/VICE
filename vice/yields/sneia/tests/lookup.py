
from __future__ import absolute_import
from ...._globals import _RECOGNIZED_ELEMENTS_
from ....testing import unittest
from .._yield_lookup import integrated_yield as fractional
from .._yield_lookup import single_detonation as single
import numbers


_STUDY_ = ["iwamoto99", "seitenzahl13", "gronow21"]
_MODEL_ = {
	"seitenzahl13":	 	["N1", "N3", "N5", "N10", "N40", "N100H", "N100",
						"N100L", "N150", "N200", "N300C", "N1600", "N100_Z0.5",
						"N100_Z0.1", "N100_Z0.01"],
	"iwamoto99": 		["W7", "W70", "WDD1", "WDD2", "WDD3", "CDD1", "CDD2"],
	"gronow21": 		["M08_03_001", "M08_03_01", "M08_03_1", "M08_03_3",
						"M08_05_001", "M08_05_01", "M08_05_1", "M08_05_3",
						"M08_10_001", "M08_10_01", "M08_10_1", "M08_10_3",
						"M09_03_001", "M09_03_01", "M09_03_1", "M09_03_3",
						"M09_05_001", "M09_05_01", "M09_05_1", "M09_05_3",
						"M09_10_001", "M09_10_01", "M09_10_1", "M09_10_3",
						"M10_02_001", "M10_02_01", "M10_02_1", "M10_02_3",
						"M10_03_001", "M10_03_01", "M10_03_1", "M10_03_3",
						"M10_05_001", "M10_05_01", "M10_05_1", "M10_05_3",
						"M10_10_001", "M10_10_01", "M10_10_1", "M10_10_3",
						"M11_05_001", "M11_05_01", "M11_05_1", "M11_05_3"]
}


@unittest
def test_single():
	"""
	vice.yields.sneia.single unit test
	"""
	def test():
		"""
		Test the single SN Ia mass yield lookup function
		"""
		status = True
		for i in _RECOGNIZED_ELEMENTS_:
			for j in _STUDY_:
				for k in _MODEL_[j]:
					try:
						x = single(i, study = j, model = k)
					except:
						return False
					status &= isinstance(x, numbers.Number)
					status &= x >= 0
					if not status: break
				if not status: break
			if not status: break
		return status
	return ["vice.yields.sneia.single", test]


@unittest
def test_fractional():
	"""
	vice.yields.sneia.fractional unit test
	"""
	def test():
		"""
		Test the fractional SN Ia mass yield function
		"""
		status = True
		for i in _RECOGNIZED_ELEMENTS_:
			for j in _STUDY_:
				for k in _MODEL_[j]:
					try:
						x = fractional(i, study = j, model = k)
					except:
						return False
					status &= isinstance(x, numbers.Number)
					status &= 0 <= x < 1
					if not status: break
				if not status: break
			if not status: break
		return status
	return ["vice.yields.sneia.fractional", test]

