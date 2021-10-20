
from __future__ import absolute_import
__all__ = [
	"calcz_history",
	"calcz_tracers",
	"zscaled_history",
	"zscaled_tracers"
]
from ....testing import unittest
from ....core.outputs import history
from ....core.outputs import stars
from ....core.dataframe._builtin_dataframes import solar_z
import numbers

r"""
Notes
-----
VICE writes each quantity to the output file with 7 significant digits,
meaning quantities that should be equal may be off by 1e-7 due to
roundoff error.
"""


@unittest
def calcz_history():
	r"""
	vice.core.dataframe.history.__getitem__.calcz unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice singlezone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.history import _ELEMENTS_
		try:
			_TEST_ = history("test")
			for i in _ELEMENTS_:
				assert isinstance(_TEST_["z(%s)" % (i)], list)
				assert all(map(lambda x: isinstance(x, numbers.Number),
					_TEST_["z(%s)" % (i)]))
				assert all(map(lambda x, y, z: abs(x - y / z) <= 1.e-7,
					_TEST_["z(%s)" % (i)], _TEST_["mass(%s)" % (i)],
					_TEST_["mgas"]))
			assert isinstance(_TEST_["y"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["y"]))
			assert all(map(lambda x, y: x == y,
				_TEST_["y"], _TEST_["z(he)"]))
		except:
			return False
		return True
	return ["vice.core.dataframe.history.__getitem__.calcz", test]


@unittest
def calcz_tracers():
	r"""
	vice.core.dataframe.tracers.__getitem__.calcz unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice multizone output
		has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.tracers import _ELEMENTS_
		try:
			_TEST_ = stars("test")
			for i in _ELEMENTS_:
				assert isinstance(_TEST_["z(%s)" % (i)], list)
				assert all(map(lambda x: isinstance(x, numbers.Number),
					_TEST_["z(%s)" % (i)]))
				assert all(map(lambda x: x >= 0, _TEST_["z(%s)" % (i)]))
			assert isinstance(_TEST_["y"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["y"]))
			assert all(map(lambda x, y: x == y, _TEST_["y"], _TEST_["z(he)"]))
		except:
			return False
		return True
	return ["vice.core.dataframe.tracers.__getitem__.calcz", test]


@unittest
def zscaled_history():
	r"""
	vice.core.dataframe.history.__getitem__.zscaled unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice singlezone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.history import _ELEMENTS_
		try:
			_TEST_ = history("test")
			assert isinstance(_TEST_["z"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["z"]))
			for i in range(len(_TEST_["z"])):
				assert abs(_TEST_["z"][i] - 0.014 * sum(
					[_TEST_["z(%s)" % (j)][i] for j in _ELEMENTS_]) / sum(
					[solar_z[j] for j in _ELEMENTS_])) <= 1.e-7
		except:
			return False
		return True
	return ["vice.core.dataframe.history.__getitem__.zscaled", test]
	

@unittest
def zscaled_tracers():
	r"""
	vice.core.dataframe.tracers.__getitem__.zscaled unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice multizone output
		has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.tracers import _ELEMENTS_
		try:
			_TEST_ = stars("test")
			assert isinstance(_TEST_["z"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["z"]))
			for i in range(len(_TEST_["z"])):
				assert abs(_TEST_["z"][i] - 0.014 * sum(
					[_TEST_["z(%s)" % (j)][i] for j in _ELEMENTS_]) / sum(
					[solar_z[j] for j in _ELEMENTS_])) <= 1.e-7
		except:
			return False
		return True
	return ["vice.core.dataframe.tracers.__getitem__.zscaled", test]

