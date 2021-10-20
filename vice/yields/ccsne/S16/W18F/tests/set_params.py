
from __future__ import absolute_import
from ......_globals import _RECOGNIZED_ELEMENTS_
from ......testing import unittest
from .... import fractional
from .... import settings


@unittest
def test():
	r"""
	Run the unit test on the set_params function in this module.
	"""
	def test_set_params():
		kwargs = {
			"m_lower": 		0.3,
			"m_upper":		80,
			"IMF": 			"salpeter"
		}
		try:
			from .. import set_params
			set_params(**kwargs)
		except:
			return False
		status = True
		for i in _RECOGNIZED_ELEMENTS_:
			status &= settings[i] == fractional(i, study = "S16/W18F",
				**kwargs)[0]
			if not status: break
		return status
	return ["vice.yields.ccsne.S16.W18F.set_params", test_set_params]

