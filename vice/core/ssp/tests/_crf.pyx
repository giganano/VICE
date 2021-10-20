# cython: language_level = 3, boundscheck = False

from __future__ import absolute_import
__all__ = ["test"]
from ...._globals import _VERSION_ERROR_
from ....testing import moduletest
from ....testing import unittest
from ....testing import generator
from .._crf import cumulative_return_fraction
from ...mlr import mlr
import math
import sys
if sys.version_info[:2] == (2, 7):
	strcomp = basestring
elif sys.version_info[:2] >= (3, 5):
	strcomp = str
else:
	_VERSION_ERROR_()
from . cimport _crf


@moduletest
def test():
	r"""
	Run the tests on the vice.cumulative_return_fraction function.
	"""
	tests = []
	for i in mlr.recognized: tests.append(mlr_generator(mlr = i)())
	tests.append(test_cumulative_return_fraction())
	tests.append(test_setup_cumulative_return_fraction())
	return ["vice.core.cumulative_return_fraction", tests]


class mlr_generator(generator):

	# Systematically generate trial calculations of the cumulative return
	# fraction for various assumptions about the mass-lifetime relation.
	# A step size of 1.e-3 is used to ensure that the assumed MLR responds
	# properly to stellar populations young enough that no stars have died
	# yet.

	def __init__(self, mlr = "larson1974"):
		self.mlr = mlr
		super().__init__("vice.core.cumulative_return_fraction [MLR :: %s]" % (
			self.mlr))

	@unittest
	def __call__(self):
		def test():
			try:
				current = mlr.setting
				mlr.setting = self.mlr
				times = [1.e-3 * i for i in range(10001)]
				status = True
				for time in times:
					x = cumulative_return_fraction(time)
					status &= not math.isnan(x)
					status &= 0 <= x <= 1
					if not status: break
				mlr.setting = current
			except:
				return False
			return status
		return [self.msg, test]

	@property
	def mlr(self):
		r"""
		Type : str

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


@unittest
def test_cumulative_return_fraction():
	"""
	Test the cumulative return fraction function at vice/src/ssp/crf.h
	"""
	return ["vice.src.ssp.crf.CRF", _crf.test_CRF]


@unittest
def test_setup_cumulative_return_fraction():
	"""
	Test the cumulative return fraction setup for singlezone simulation at
	vice/src/ssp/crf.h
	"""
	return ["vice.src.ssp.crf.setup_CRF", _crf.test_setup_CRF]

