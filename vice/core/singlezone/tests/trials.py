"""
This file runs trial tests of the singlezone object to ensure that each
attribute which can vary by type does not produce an error at runtime.
"""

from __future__ import absolute_import
__all__ = [
	"test"
]
from ...._globals import _VERSION_ERROR_
from ....testing import moduletest
from ....testing import unittest
from ....testing import generator
from ...outputs import output
from ..singlezone import singlezone
from ...mlr import mlr
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
	_OUTTIMES_ = np.linspace(0, 1, 21)
except (ModuleNotFoundError, ImportError):
	_OUTTIMES_ = [0.05 * i for i in range(21)]


"""
Below are each of the parameters that either have a limited range of values
or may vary by type. The singlezone object is tested by running one of each
and ensuring that the simulation runs under each parameter.
"""
_MODES_ = ["ifr", "sfr", "gas"]
_IMF_ = ["kroupa", "salpeter", lambda m: m**-2]
_ETA_ = [2.5, lambda t: 2.5 * math.exp( -t / 4.0 )]
_ZIN_ = [0, 1.0e-8, lambda t: 1.0e-8 * (t / 10.0), {
	"o":		lambda t: 0.0057 * (t / 10.0),
	"fe": 		0.0013
}]
_RECYCLING_ = ["continuous", 0.4]
_RIA_ = ["plaw", "exp", lambda t: t**-1.5]
_TAU_STAR_ = [2.0,
	lambda t: 2.0 + t / 10.0,
	lambda t, m: 2.0 * (m / 3.0)**0.5]
_SCHMIDT_ = [False, True]


class attribute_generator(generator):

	# Systematically generate trial tests for the singlezone object.

	def __init__(self, msg, **kwargs):
		super().__init__(msg, **kwargs)
		self._sz = singlezone(name = "test", dt = 0.05, **kwargs)

	@unittest
	def __call__(self):
		def test():
			try:
				self._sz.run(_OUTTIMES_, overwrite = True)
			except:
				return False
			status = True
			if self._sz.schmidt:
				try:
					out = output("test")
				except:
					return None
				tau_star = [1.e-9 * a / b if b else float("inf") for a, b in
					zip(out.history["mgas"], out.history["sfr"])]
				status &= all([i >= self._sz.tau_star for i in tau_star])
			else:
				pass
			return status
		return [self.msg, test]


class mlr_generator(generator):

	# Systematically generate trial tests for the singlezone object with
	# different mass-lifetime relations. A timestep size of 1 Myr is used to
	# ensure that the assumed MLR responds properly to stellar populations
	# young enough that no stars have died yet.

	def __init__(self, mlr = "larson1974"):
		self.mlr = mlr
		super().__init__("vice.core.singlezone [MLR :: %s]" % (self.mlr))
		self._sz = singlezone(name = "test", elements = ["fe", "sr", "o"],
			dt = 0.001)

	@unittest
	def __call__(self):
		def test():
			try:
				current = mlr.setting
				mlr.setting = self.mlr
				# stop at 500 Myr, no need to go longer since this already gets
				# into the regime where AGB stars will be ejecting yields
				outtimes = [0.01 * i for i in range(51)]
				out = self._sz.run(outtimes, overwrite = True, capture = True)
				mlr.setting = current
			except:
				return False
			status = True
			for i in range(len(out.history["time"])):
				status &= not math.isnan(out.history["mass(fe)"][i])
				status &= not math.isnan(out.history["mass(sr)"][i])
				status &= not math.isnan(out.history["mass(o)"][i])
				if not status: break
			return status
		return [self.msg, test]

	@property
	def mlr(self):
		r"""
		Type : ``str``

		Default : "larson1974"

		The MLR setting to test the singlezone object with.
		"""
		return self._mlr

	@mlr.setter
	def mlr(self, value):
		if isinstance(value, strcomp):
			if value.lower() in mlr.recognized:
				self._mlr = value.lower()
			else:
				raise ValueError("Unrecognized MLR: %s" % (value))
		else:
			raise TypeError("MLR must be of type str. Got: %s" % (type(value)))


@moduletest
def test():
	"""
	Run the trial tests of the singlezone object
	"""
	trials = []
	for i in _MODES_:
		trials.append(attribute_generator(
			"vice.core.singlezone [mode :: %s]" % (str(i)), mode = i)())
	for i in _IMF_:
		trials.append(attribute_generator(
			"vice.core.singlezone [IMF :: %s]" % (str(i)), IMF = i)())
	for i in _ETA_:
		trials.append(attribute_generator(
			"vice.core.singlezone [eta :: %s]" % (str(i)), eta = i)())
	for i in _ZIN_:
		trials.append(attribute_generator(
			"vice.core.singlezone [Zin :: %s]" % (str(i)), Zin = i)())
	for i in _RECYCLING_:
		trials.append(attribute_generator(
			"vice.core.singlezone [recycling :: %s]" % (str(i)),
			recycling = i)())
	for i in _RIA_:
		trials.append(attribute_generator(
			"vice.core.singlezone [RIa :: %s]" % (str(i)), RIa = i)())
	for i in _TAU_STAR_:
		trials.append(attribute_generator(
			"vice.core.singlezone [tau_star :: %s]" % (str(i)),
			tau_star = i)())
	for i in _SCHMIDT_:
		trials.append(attribute_generator(
			"vice.core.singlezone [schmidt :: %s]" % (str(i)), schmidt = i)())
	for i in mlr.recognized: trials.append(mlr_generator(mlr = i)())
	return ["vice.core.singlezone trial tests", trials]

