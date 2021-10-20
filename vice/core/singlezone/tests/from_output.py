
from __future__ import absolute_import
__all__ = ["test_from_output"]
from ..singlezone import singlezone
from ....testing import unittest
import os


@unittest
def test_from_output():
	r"""
	vice.singlezone.from_output unittest
	"""
	def test():
		try:
			singlezone(name = "test").run([0.01 * i for i in range(1001)],
				overwrite = True)
			test_ = singlezone.from_output("test")
		except:
			return False
		return isinstance(test_, singlezone) and test_.name == "test"
	return ["vice.singlezone.from_output", test]

