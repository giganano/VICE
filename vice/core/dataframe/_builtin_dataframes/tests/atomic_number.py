
from __future__ import absolute_import
__all__ = ["test_atomic_number"]
from ....._globals import _RECOGNIZED_ELEMENTS_
from .....testing import unittest
from ..atomic_number import atomic_number
import numbers


@unittest
def test_atomic_number():
	"""
	Atomic number built-in dataframe unit test
	"""
	def test():
		""""
		Test the atomic number dataframe
		"""
		try:
			for i in _RECOGNIZED_ELEMENTS_:
				assert isinstance(atomic_number[i], numbers.Number)
				assert atomic_number[i] % 1 == 0
		except:
			return False
		return True
	return ["vice.core.dataframe._builtin_datafarmes.atomic_number", test]

