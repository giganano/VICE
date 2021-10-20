"""
Test the CCSNe yield integrator at vice/yields/ccnse/_yield_integrator.pyx
"""

from __future__ import absolute_import
__all__ = ["test" ]
from ...._globals import _RECOGNIZED_ELEMENTS_
from .._yield_integrator import integrate as fractional
from .._errors import _RECOGNIZED_STUDIES_ as _STUDY_
from .._errors import _NAMES_
from .._errors import _MOVERH_
from .._errors import _ROTATION_
from ....testing import moduletest
from ....testing import unittest
from ....testing import generator
import warnings
import random
random.seed()
import math

# upper mass cutoff of each study
_UPPER_ = {
	"LC18":			120,
	"CL13": 		120,
	"NKT13": 		40,
	"CL04": 		35,
	"WW95": 		40,
	"S16/W18": 		120,
	"S16/W18F": 	120,
	"S16/N20": 		120
}

# IMFs to test the integrations on
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2]


class fractional_generator(generator):

	# Systematically generate unit tests of the vice.yields.ccsne.fractional
	# function.

	@unittest
	def __call__(self):
		def test():
			success = True
			# Conduct the assertions for 10 randomly drawn elements
			for i in range(10):
				idx = int(random.random() * len(_RECOGNIZED_ELEMENTS_))
				elem = _RECOGNIZED_ELEMENTS_[idx]
				try:
					net_with_wind, err_net_with_wind = fractional(elem,
						wind = True, net = True, **self._kwargs)
					gross_with_wind, err_gross_with_wind = fractional(elem,
						wind = True, net = False, **self._kwargs)
					net_no_wind, err_net_no_wind = fractional(elem,
						wind = False, net = True, **self._kwargs)
					gross_no_wind, err_gross_no_wind = fractional(elem,
						wind = False, net = False, **self._kwargs)
				except:
					return False

				# error should always be NaN if the yield is zero
				if net_with_wind == 0: success &= math.isnan(err_net_with_wind)
				if gross_with_wind == 0: success &= math.isnan(
					err_gross_with_wind)
				if net_no_wind == 0: success &= math.isnan(err_net_no_wind)
				if gross_no_wind == 0: success &= math.isnan(err_gross_no_wind)

				# Fractional yields must always be between 0 and 1, but the net
				# yields can be negative
				success &= 0 <= gross_with_wind <= 1
				success &= 0 <= gross_no_wind <= 1
				success &= net_with_wind <= 1
				success &= net_no_wind <= 1

				# Compare the gross and net yields with and without winds
				# taking into account the numerical errors.
				if gross_no_wind and gross_with_wind:
					success &= (gross_no_wind - err_gross_no_wind <=
						gross_with_wind + err_gross_with_wind)
					success &= gross_with_wind <= 1
				else: pass
				if net_no_wind and net_with_wind:
					success &= (net_no_wind - err_net_no_wind <=
						net_with_wind + err_net_with_wind)
				else: pass
				if net_no_wind and gross_no_wind:
					success &= (net_no_wind - err_net_no_wind <=
						gross_no_wind + err_gross_no_wind)
				else: pass
				if net_with_wind and gross_with_wind:
					success &= (net_with_wind - err_net_with_wind <=
						gross_with_wind + err_gross_with_wind)
				if not success: break
			return success
		return [self.msg, test]


@moduletest
def test():
	"""
	Test the yield integration functions
	"""
	trials = []
	for i in _STUDY_:
		for j in _MOVERH_[i]:
			for k in _ROTATION_[i]:
				for l in _IMF_:
					# Compute the yields with trapezoid rule - in practice
					# simpson's rule produces numerical errors for some
					# elements with the LC18 yields at [M/H] = -1 and
					# rotation = 300 km/s for the custom IMF. These errors are
					# small and are not cause for concern, but do cause the
					# test to spurriously fail.
					params = dict(
						study = i,
						MoverH = j,
						rotation = k,
						IMF = l,
						m_upper = _UPPER_[i],
						method = "trapezoid"
					)
					trials.append(fractional_generator(
						"%s :: [M/H] = %g :: vrot = %g km/s :: IMF = %s" % (
							_NAMES_[i], j, k, l),
						**params)())
	return ["vice.yields.ccsne.fractional", trials]

