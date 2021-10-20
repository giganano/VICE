
from __future__ import absolute_import
__all__ = ["test_mdf"]
from ....testing import unittest
from ...dataframe import base as dataframe
from ...singlezone import singlezone
from .. import mdf


@unittest
def test_mdf():
	r"""
	vice.mdf unit test
	"""
	def test():
		try:
			singlezone.singlezone(name = "test").run(
				[0.01 * i for i in range(1001)],
				overwrite = True
			)
			test_ = mdf("test")
		except:
			return False
		return isinstance(test_, dataframe)
	return ["vice.mdf", test]

