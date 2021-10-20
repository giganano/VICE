
from __future__ import absolute_import
__all__ = [
	"calclogz_history",
	"calclogz_tracers",
	"logzscaled_history",
	"logzscaled_tracers"
]
from ....testing import unittest
from ....core.outputs import history
from ....core.outputs import stars
from ....core.dataframe._builtin_dataframes import solar_z
import math as m
import numbers

r"""
Notes
-----
VICE writes each quantity to the output file with 7 significant digits,
meaning quantities that should be equal may be off by 1e-7 due to
roundoff error.
"""


@unittest
def calclogz_history():
	r"""
	vice.core.dataframe.history.__getitem__.calclogz unit test
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
				assert isinstance(_TEST_["[%s/h]" % (i)], list)
				assert all(map(lambda x: isinstance(x, numbers.Number),
					_TEST_["[%s/h]" % (i)]))
				assert all(map(lambda x, y:
					abs(x - m.log10(y / solar_z[i])) <= 1.e-7,
					_TEST_["[%s/h]" % (i)][1:], _TEST_["z(%s)" % (i)][1:]))
				for j in _ELEMENTS_:
					assert isinstance(_TEST_["[%s/%s]" % (i, j)], list)
					assert all(map(lambda x: isinstance(x, numbers.Number),
						_TEST_["[%s/%s]" % (i, j)]))
					assert all(map(lambda x, y, z: abs(x - (y - z)) <= 1.e-7,
						_TEST_["[%s/%s]" % (i, j)][1:],
						_TEST_["[%s/h]" % (i)][1:],
						_TEST_["[%s/h]" % (j)][1:]))
		except:
			return False
		return True
	return ["vice.core.dataframe.history.__getitem__.calclogz", test]


@unittest
def calclogz_tracers():
	r"""
	vice.core.dataframe.tracers.__getitem__.calclogz unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice multizone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.tracers import _ELEMENTS_
		try:
			_TEST_ = stars("test")
			first_nonzero_idx = 0
			while _TEST_["z(fe)"][first_nonzero_idx] == 0:
				first_nonzero_idx += 1
			for i in _ELEMENTS_:
				assert isinstance(_TEST_["[%s/h]" % (i)], list)
				assert all(map(lambda x: isinstance(x, numbers.Number),
					_TEST_["[%s/h]" % (i)]))
				assert all(map(lambda x, y:
					abs(x - m.log10(y / solar_z[i])) <= 1.e-7,
					_TEST_["[%s/h]" % (i)][first_nonzero_idx:],
					_TEST_["z(%s)" % (i)][first_nonzero_idx:]))
				for j in _ELEMENTS_:
					assert isinstance(_TEST_["[%s/%s]" % (i, j)], list)
					assert all(map(lambda x: isinstance(x, numbers.Number),
						_TEST_["[%s/%s]" % (i, j)]))
					assert all(map(lambda x, y, z: abs(x - (y - z)) <= 1.e-7,
						_TEST_["[%s/%s]" % (i, j)][first_nonzero_idx:],
						_TEST_["[%s/h]" % (i)][first_nonzero_idx:],
						_TEST_["[%s/h]" % (j)][first_nonzero_idx:]))
		except:
			return False
		return True
	return ["vice.core.dataframe.tracers.__getitem__.calclogz", test]


@unittest
def logzscaled_history():
	r"""
	vice.core.dataframe.history.__getitem__.logzscaled unittest
	"""
	def test():
		r"""
		This function will only be called after the test.vice singlezone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.history import _ELEMENTS_
		try:
			_TEST_ = history("test")
			assert isinstance(_TEST_["[m/h]"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["[m/h]"]))
			assert all(map(lambda x, y: abs(x - m.log10(y / 0.014)) <= 1.e-7,
				_TEST_["[m/h]"][1:], _TEST_["z"][1:]))
		except:
			return False
		return True
	return ["vice.core.dataframe.history.__getitem__.logzscaled", test]


@unittest
def logzscaled_tracers():
	r"""
	vice.core.dataframe.tracers.__getitem__.logzscaled unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice multizone
		output has been produced by the module test which calls this.
		"""
		from ....core.dataframe.tests.tracers import _ELEMENTS_
		try:
			_TEST_ = stars("test")
			first_nonzero_idx = 0
			while _TEST_["z(fe)"][first_nonzero_idx] == 0:
				first_nonzero_idx += 1
			assert isinstance(_TEST_["[m/h]"], list)
			assert all(map(lambda x: isinstance(x, numbers.Number),
				_TEST_["[m/h]"]))
			assert all(map(lambda x, y: abs(x - m.log10(y / 0.014)) <= 1.e-7,
				_TEST_["[m/h]"][first_nonzero_idx:],
				_TEST_["z"][first_nonzero_idx:]))
		except:
			return False
		return True
	return ["vice.core.dataframe.tracers.__getitem__.logzscaled", test]

