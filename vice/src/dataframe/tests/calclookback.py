
from __future__ import absolute_import
__all__ = ["calclookback_history", "calclookback_tracers"]
from ....testing import unittest
from ....core.outputs import stars
from ....core.outputs import history
import numbers

r"""
Notes
-----
VICE writes each quantity to the output file with 7 significant digits,
meaning quantities that should be equal may be off by 1e-7 due to
roundoff error.
"""


@unittest
def calclookback_history():
	r"""
	vice.core.dataframe.history.__getitem__.calclookback unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice singlezone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.history import _ELEMENTS_
		try:
			_TEST_ = history("test")
			assert isinstance(_TEST_["lookback"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["lookback"]))
			assert all(map(lambda x, y:
				abs(x - (max(_TEST_["time"]) - y)) <= 1.e-7,
				_TEST_["lookback"], _TEST_["time"]))
		except:
			return False
		return True
	return ["vice.core.dataframe.history.__getitem__.calclookback", test]


@unittest
def calclookback_tracers():
	r"""
	vice.core.dataframe.tracers.__getitem__.calclookback unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice multizone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.tracers import _ELEMENTS_
		try:
			_TEST_ = stars("test")
			assert isinstance(_TEST_["age"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["age"]))
			assert all(map(lambda x, y:
				abs(x - (max(_TEST_["formation_time"]) - y)) <= 1.e-7,
				_TEST_["age"], _TEST_["formation_time"]))
		except:
			return False
		return True
	return ["vice.core.dataframe.tracers.__getitem__.calclookback", test]

