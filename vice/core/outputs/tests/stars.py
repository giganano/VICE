
from __future__ import absolute_import
__all__ = ["test_stars"]
from ....testing import unittest
from ...dataframe import base as dataframe
from .._tracers import tracers


@unittest
def test_stars():
	r"""
	vice.stars unit test
	"""
	from ...multizone import multizone
	def test():
		try:
			multizone(name = "test", n_zones = 3).run(
				[0.01 * i for i in range(1001)],
				overwrite = True
			)
			test_ = tracers("test")
		except:
			return False
		return isinstance(test_, dataframe)
	return ["vice.stars", test]

