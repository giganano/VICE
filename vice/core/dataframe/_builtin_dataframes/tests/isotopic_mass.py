
from __future__ import absolute_import
__all__ = ["test_isotopic_mass"]
from ....._globals import _RECOGNIZED_ELEMENTS_
from .....testing import unittest
from ..isotopic_mass import isotopic_mass


@unittest
def test_isotopic_mass():
	r"""
	Isotopic mass built-in dataframe unit test
	"""
	def test():
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert isinstance(isotopic_mass[i], dict)
				assert all(map(lambda x: i in x,
					isotopic_mass[i].keys()))
				assert all(map(lambda x: isinstance(x, int),
					isotopic_mass[i].values()))
		except:
			return False
		return True
	return ["vice.core.datafarme._builtin_dataframes.isotopic_mass", test]

