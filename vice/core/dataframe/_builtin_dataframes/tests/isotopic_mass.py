
from __future__ import absolute_import
__all__ = ["test_isotopic_mass"]
from ....._globals import _RECOGNIZED_ELEMENTS_
from ....._globals import _RECOGNIZED_ISOTOPES_
from .....testing import unittest
from ..._base import base
from ..isotopic_mass import isotopic_mass


@unittest
def test_isotopic_mass():
	r"""
	Isotopic mass built-in dataframe unit test
	"""
	def test():
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert isinstance(isotopic_mass[i], base)
				assert all(map(lambda x: x in _RECOGNIZED_ISOTOPES_,
					isotopic_mass[i].keys()))
				assert all(map(lambda x: isinstance(x, float),
					isotopic_mass[i].todict().values()))
		except:
			return False
		return True
	return ["vice.core.datafarme._builtin_dataframes.isotopic_mass", test]

