
from __future__ import absolute_import
__all__ = ["test_solar_z"]
from ....._globals import _RECOGNIZED_ELEMENTS_
from .....testing import unittest
from ..solar_z import solar_z
import numbers


@unittest
def test_solar_z():
	"""
	Solar_z built-in dataframe unit test
	"""
	def test():
		"""
		Test the solar_z dataframe
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert isinstance(solar_z[i], numbers.Number)
				assert 0 < solar_z[i] < 1
		except:
			return False
		return 0 < sum([solar_z[i] for i in _RECOGNIZED_ELEMENTS_]) < 1
	return ["vice.core.dataframe._builtin_dataframes.solar_z", test]

