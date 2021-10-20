
from __future__ import absolute_import
__all__ = ["test_stable_isotopes"]
from ....._globals import _RECOGNIZED_ELEMENTS_
from .....testing import unittest
from ..stable_isotopes import stable_isotopes


@unittest
def test_stable_isotopes():
	r"""
	Stable isotopes built-in dataframe unit test
	"""
	def test():
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert isinstance(stable_isotopes[i], list)
				assert all(map(lambda x: isinstance(x, int),
					stable_isotopes[i]))
		except:
			return False
		return True
	return ["vice.core.datafarme._builtin_dataframes.stable_isotopes", test]

