r"""
This file implements the functional equivalence test, which ensures that
functional yield attributes which return the same value as a numerical setting
(or in the case of the AGB yield settings, an un-modified interpolator),
predict numerically similar results.

In practice, this tests passes with a percent difference in the predicted
masses of less than a part per million.
"""

from ...core import singlezone
from ...testing import unittest
from .. import agb
from .. import ccsne
from .. import sneia

_OUTTIMES_ = [0.05 * i for i in range(201)]

_CCSN_YIELD_O_ = ccsne.settings['o']
_CCSN_YIELD_FE_ = ccsne.settings['fe']
_CCSN_YIELD_SR_ = ccsne.settings['sr']

_SNIA_YIELD_O_ = sneia.settings['o']
_SNIA_YIELD_FE_ = sneia.settings['fe']
_SNIA_YIELD_SR_ = sneia.settings['sr']


def ccsn_yield_o(z):
	r"""
	Returns the current CCSN yield setting for oxygen
	"""
	return _CCSN_YIELD_O_

def ccsn_yield_fe(z):
	r"""
	Returns the current CCSN yield setting for iron
	"""
	return _CCSN_YIELD_FE_

def ccsn_yield_sr(z):
	r"""
	Returns the current CCSN yield setting for strontium
	"""
	return _CCSN_YIELD_SR_

def snia_yield_o(z):
	r"""
	Returns the current SN Ia yield setting for oxygen
	"""
	return _SNIA_YIELD_O_

def snia_yield_fe(z):
	r"""
	Returns the current SN Ia yield setting for iron
	"""
	return _SNIA_YIELD_FE_

def snia_yield_sr(z):
	r"""
	Returns the current SN Ia yield setting for strontium
	"""
	return _SNIA_YIELD_SR_

class agb_interpolator_mimic(agb.interpolator):

	# The AGB yield calculator forces yields to zero if a negative yield is
	# calculated for progenitor masses < 1.5 Msun to avoid numerical artifacts.
	# The agb.interpolator objects does not do this, so this functionality is
	# duplicated here in a subclass for testing purposes.

	def __call__(self, mass, metallicity):
		y = super().__call__(mass, metallicity)
		if mass < 1.5 and y < 0:
			return 0
		else:
			return y


@unittest
def equivalence_test():
	r"""
	equivalence test for functional yields.
	"""
	def test():
		agb.settings['o'] = "cristallo11"
		agb.settings['fe'] = "cristallo11"
		agb.settings['sr'] = "cristallo11"
		attrs = {
			"name": 		"test",
			"elements": 	["fe", "sr", "o"],
			"dt": 			0.05
		}
		try:
			out1 = singlezone.singlezone(**attrs).run(_OUTTIMES_,
				overwrite = True, capture = True)
		except:
			return None
		try:
			ccsne.settings['o'] = ccsn_yield_o
			ccsne.settings['fe'] = ccsn_yield_fe
			ccsne.settings['sr'] = ccsn_yield_sr
			sneia.settings['o'] = snia_yield_o
			sneia.settings['fe'] = snia_yield_fe
			sneia.settings['sr'] = snia_yield_sr
			agb.settings['o'] = agb_interpolator_mimic('o')
			agb.settings['fe'] = agb_interpolator_mimic('fe')
			agb.settings['sr'] = agb_interpolator_mimic('sr')
		except:
			return None
		try:
			out2 = singlezone.singlezone(**attrs).run(_OUTTIMES_,
				overwrite = True, capture = True)
		except:
			return None
		status = True
		for i in range(len(out1.history["time"])):
			for elem in ["fe", "sr", "o"]:
				col = "mass(%s)" % (elem)
				if out1.history[col][i]:
					percent_diff = abs(
						(out1.history[col][i] - out2.history[col][i]) /
						out1.history[col][i])
				else:
					percent_diff = abs(out2.history[col][i])
				status &= percent_diff <= 1.e-6
				if not status: break
			if not status: break
		return status
	return ["vice.yields edge case : functional equivalence", test]

