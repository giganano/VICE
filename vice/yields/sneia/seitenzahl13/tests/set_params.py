
from __future__ import absolute_import
from ....._globals import _RECOGNIZED_ELEMENTS_
from .....testing import unittest
from ... import fractional
from ... import settings


@unittest
def test():
	r"""
	Run the unit test on the set_params function in this module
	"""
	def test_set_params():
		kwargs = {
			"model": "N100L",
			"n": 1.5e-03
		}
		try:
			from .. import set_params
		except:
			return None
		try:
			set_params(**kwargs)
		except:
			return False
		status = True
		for i in _RECOGNIZED_ELEMENTS_:
			status &= settings[i] == fractional(i, study = "seitenzahl13",
				**kwargs)
			if not status: break
		return status
	return ["vice.yields.sneia.seitenzahl13.set_params", test_set_params]

