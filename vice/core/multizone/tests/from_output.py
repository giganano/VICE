
from __future__ import absolute_import
__all__ = ["test_from_output"]
from ..multizone import multizone
from ....testing import unittest
import os


@unittest
def test_from_output():
	r"""
	vice.multizone.from_output unittest
	"""
	def test():
		try:
			multizone(name = "test", n_zones = 3).run(
				[0.01 * i for i in range(1001)],
				overwrite = True)
			test_ = multizone.from_output("test")
		except:
			return False
		return isinstance(test_, multizone) and test_.name == "test"
	return ["vice.multizone.from_output", test]

