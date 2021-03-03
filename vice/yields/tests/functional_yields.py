r""" 
This file implements the functional equivalence test, which ensures that 
functional yield attributes which return the same value as a numerical setting 
(or in the case of the AGB yield settings, an un-modified interpolator), 
predict numerically similar results. 

In practice, this tests passes with a percent difference in the predicted 
masses of a few times 10^-4. 
""" 

from ...core import singlezone 
from ...testing import unittest 
from .. import agb 
from .. import ccsne 
from .. import sneia 

_OUTTIMES_ = [0.05 * i for i in range(201)] 
_CCSN_YIELD_ = ccsne.settings['o'] 
_SNIA_YIELD_ = sneia.settings['o'] 


def ccsn_yield(z): 
	r""" 
	Returns the current CCSN yield setting 
	""" 
	return _CCSN_YIELD_ 


def snia_yield(z): 
	r""" 
	Returns the current SN Ia yield setting 
	""" 
	return _SNIA_YIELD_ 


@unittest 
def equivalence_test(): 
	r""" 
	equivalence test for functional yields. 
	""" 
	def test(): 
		attrs = {
			"name": 		"test", 
			"elements": 	['o'], 
			"dt": 			0.05 
		}
		try: 
			out1 = singlezone.singlezone(**attrs).run(_OUTTIMES_, 
				overwrite = True, capture = True) 
		except: 
			return None 
		try: 
			ccsne.settings['o'] = ccsn_yield 
			sneia.settings['o'] = snia_yield 
			agb.settings['o'] = agb.interpolator('o') 
		except: 
			return None 
		try: 
			out2 = singlezone.singlezone(**attrs).run(_OUTTIMES_, 
				overwrite = True, capture = True) 
		except: 
			return None 
		status = True 
		for i in range(len(out1.history["time"])): 
			if out1.history["mass(o)"][i]: 
				percent_diff = abs(
					(out1.history["mass(o)"][i] - out2.history["mass(o)"][i]) / 
					out1.history["mass(o)"][i]) 
			else: 
				percent_diff = abs(out2.history["mass(o)"][i]) 
			status &= percent_diff <= 2.e-4 
			if not status: break 
		return status 
	return ["vice.yields edge case : functional equivalence", test] 

