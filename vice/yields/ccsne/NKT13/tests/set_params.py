
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
			"m_lower": 0.3,
			"m_upper": 40,
			"MoverH": 0.15,
			"IMF": "salpeter"
		}
		try:
			from .. import set_params
			set_params(**kwargs)
		except:
			return False
		status = True
		for i in _RECOGNIZED_ELEMENTS_:
			if settings[i] != fractional(i, study = "NKT13", **kwargs)[0]:
				status = False
				break
		return status
	return ["vice.yields.ccsne.NKT13.set_params", test_set_params]

