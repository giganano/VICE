
from __future__ import absolute_import
__all__ = [
	"test",
	"test_singlezone_open_files"
]
from ....testing import moduletest
from ....testing import unittest
from ...singlezone.tests._singlezone import singlezone_tester


@moduletest
def test():
	r"""
	vice.src.io.singlezone module test
	"""
	return ["vice.src.io.singlezone",
		[
			test_singlezone_open_files()
		]
	]


@unittest
def test_singlezone_open_files():
	r"""
	vice.src.io.singlezone.singlezone_open_files unit test
	"""
	def test_():
		try:
			_TEST_ = singlezone_tester()
		except:
			return None
		return _TEST_.test_singlezone_open_files()
	return ["vice.src.io.singlezone.singlezone_open_files", test_]

