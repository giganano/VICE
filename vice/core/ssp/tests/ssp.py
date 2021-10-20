"""
Test the single population enrichment function

User access of this code is strongly discouraged
"""

from __future__ import absolute_import
__all__ = [
	"test"
]
from ...._globals import _RECOGNIZED_ELEMENTS_
from ...._globals import _VERSION_ERROR_
from ...dataframe._builtin_dataframes import atomic_number
from .._ssp import single_stellar_population
from ....yields import agb
from ....testing import moduletest
from ....testing import unittest
from ....testing import generator
from ...mlr import mlr
import math
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()


"""
The IMF and RIa are the only parameters to the single_stellar_population
function which have a limited range of values or may vary by type. The
function is tested by ensuring that it runs under all possible combinations
"""
_MSTAR_ = 1.e6
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2]
_RIA_ = ["plaw", "exp", lambda t: t**-1.5]


class ssp_generator(generator):

	# Systematically generate tests for different parameters of the
	# single_stellar_population function.

	@unittest
	def __call__(self):
		def test():
			success = True
			for elem in _RECOGNIZED_ELEMENTS_:
				current_agb_setting = agb.settings[elem]
				agb.settings[elem] = "cristallo11"
				try:
					mass, times = single_stellar_population(elem,
						**self._kwargs)
					if mass[-1] > _MSTAR_: success = False
				except:
					success = False
				if atomic_number[elem] <= 28:
					agb.settings[elem] = "karakas10"
					try:
						mass, times = single_stellar_population(elem,
							**self._kwargs)
						if mass[-1] > _MSTAR_: success = False
					except:
						success = False
				else:
					continue
				agb.settings[elem] = current_agb_setting
			return success
		return [self.msg, test]


class mlr_generator(generator):

	# Systematically generate trial tests of the single_stellar_population
	# function for the various mass-lifetime relations built into VICE.
	# A timestep size of 1 Myr is used to ensure that the assumed MLR responds
	# properly to stellar populations young enough that no stars have died yet.

	def __init__(self, mlr = "larson1974"):
		self.mlr = mlr
		super().__init__("vice.core.single_stellar_population [MLR :: %s]" % (
			self.mlr))

	@unittest
	def __call__(self):
		def test():
			success = True
			try:
				current = mlr.setting
				mlr.setting = self.mlr
				for elem in _RECOGNIZED_ELEMENTS_:
					mass, times = single_stellar_population(elem, time = 1,
						dt = 1.e-3)
					success &= all([not math.isnan(_) for _ in mass])
					if not success: break
				mlr.setting = current
			except:
				return False
			return success
		return [self.msg, test]


@moduletest
def test():
	"""
	Run the trial tests of the single_stellar_population function
	"""
	trials = []
	for i in _IMF_:
		trials.append(ssp_generator(
			"vice.core.single_stellar_population [IMF :: %s]" % (str(i)),
			IMF = i, time = 3)())
	for i in _RIA_:
		trials.append(ssp_generator(
			"vice.core.single_stellar_population [RIa :: %s]" % (str(i)),
			RIa = i, time = 3)())
	for i in mlr.recognized: trials.append(mlr_generator(mlr = i)())
	return ["vice.core.single_stellar_population trial tests", trials]

