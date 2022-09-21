r"""
This file runs various sanity checks on singlezone models, particularly for
helium. If helium is assigned the same yields as oxygen, then the helium
abundance above the primordial abundance should evolve the same as the oxygen
abundance. This also checks for numerical artifacts in starburst scenarios.
"""

__all__ = ["test"]
from ...._globals import _VERSION_ERROR_
from ....testing import moduletest
from ....testing import unittest
from ....testing import generator
from .... import yields
from ...outputs import output
from ...dataframe._builtin_dataframes import primordial
from ..singlezone import singlezone
import math
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	import numpy as np
	_OUTTIMES_ = np.linspace(0, 10, 1001)
except (ModuleNotFoundError, ImportError):
	_OUTTIMES_ = [0.01 * _ for _ in range(1001)]


def ifrburst(t):
	r"""
	A simple infall-burst model for sanity checks on the helium abundance
	"""
	if 5 <= t < 5.01:
		return 500
	else:
		return 9.1

def sfrburst(t):
	r"""
	A simple starburst model for sanity checks on the helium abundance
	"""
	if t < 5:
		return 100
	else:
		return 100 + 50 * np.exp(-(t - 5) / 2)


class helium_smoothsfh_generator(generator):

	# Systematically generate sanity checks where helium is the same as oxygen

	def __init__(self, msg, **kwargs):
		super().__init__(msg, **kwargs)
		self._sz = singlezone(name = "test", dt = 0.01, **kwargs)

	@unittest
	def __call__(self):
		def test():
			self.setup_yields()
			try:
				out = self._sz.run(_OUTTIMES_, overwrite = True, capture = True)
			except:
				self.reset_yields()
				return False
			deltay = [_ - primordial["he"] for _ in out.history["y"]]
			oxygen = out.history["z(o)"]
			status = True
			for i in range(len(deltay)):
				if oxygen[i]:
					percent_diff = abs((oxygen[i] - deltay[i]) / oxygen[i])
					status &= percent_diff < 1.e-3
				else:
					status &= abs(deltay[i]) < 1.e-15 # floating point errors
				if not status: break
			self.reset_yields()
			return status
		return [self.msg, test]

	def setup_yields(self):
		self._current_o_yields = []
		self._current_he_yields = []
		for channel in [yields.ccsne, yields.sneia, yields.agb]:
			self._current_o_yields.append(channel.settings['o'])
			self._current_he_yields.append(channel.settings['he'])
		yields.ccsne.settings['o'] = 0.015
		yields.sneia.settings['o'] = 0
		yields.agb.settings['o'] = lambda m, z: 0
		yields.ccsne.settings['he'] = 0.015
		yields.sneia.settings['he'] = 0
		yields.agb.settings['he'] = lambda m, z: 0

	def reset_yields(self):
		# order of this list must match for-loop in setup_yields
		channels = [yields.ccsne, yields.sneia, yields.agb]
		for i in range(3):
			channels[i].settings['o'] = self._current_o_yields[i]
			channels[i].settings['he'] = self._current_he_yields[i]


class helium_burstysfh_generator(generator):

	# Systematically generate sanity checks to look for numerical artifacts in
	# the helium abundance for bursty SFHs

	def __init__(self, msg, **kwargs):
		super().__init__(msg, **kwargs)
		self._sz = singlezone(name = "test", dt = 0.01, **kwargs)

	@unittest
	def __call__(self):
		def test():
			try:
				out = self._sz.run(_OUTTIMES_, overwrite = True, capture = True)
			except:
				return False
			helium = out.history["y"]
			status = True
			maxdiff = 0.1
			for i in range(1, len(helium) - 1):
				# call it a numerical artifact if the helium abundance spikes
				# with a >= 10% percent difference between the current value
				# and *both* the values immediately before and after it
				percent_diff_1 = abs((helium[i] - helium[i - 1]) / helium[i])
				percent_diff_2 = abs((helium[i] - helium[i + 1]) / helium[i])
				status &= percent_diff_1 < maxdiff and percent_diff_2 < maxdiff
				if not status: break
			return status
		return [self.msg, test]


@moduletest
def test():
	trials = []
	kwargs = {
		"elements": ["he", "o", "fe"],
		"recycling": 0.4
	}
	for mode in ["ifr", "sfr", "gas"]:
		kwargs["mode"] = mode
		trials.append(helium_smoothsfh_generator(
			"sanity check :: helium smooth SFH [mode :: %s]" % (mode),
			**kwargs)())
	for mode in ["ifr", "sfr", "gas"]:
		kwargs["mode"] = mode
		kwargs["func"] = ifrburst if mode == "ifr" else sfrburst
		trials.append(helium_burstysfh_generator(
			"sanity check :: helium bursty SFH [mode :: %s]" % (mode),
			**kwargs)())
	return ["vice.core.singlezone sanity checks", trials]

