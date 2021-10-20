
from __future__ import absolute_import
from ....testing import moduletest
from ....testing import unittest
from ..interp_scheme_2d import interp_scheme_2d
import random


_TEST_X_VALUES_ = list(range(100))
_TEST_Y_VALUES_ = list(range(200))
_TEST_Z_VALUES_ = len(_TEST_X_VALUES_) * [None]
for i in range(len(_TEST_Z_VALUES_)):
	_TEST_Z_VALUES_[i] = len(_TEST_Y_VALUES_) * [0.]
	for j in range(len(_TEST_Z_VALUES_[i])):
		_TEST_Z_VALUES_[i][j] = _TEST_X_VALUES_[i] + _TEST_Y_VALUES_[j]


@moduletest
def test():
	r"""
	vice.toolkit.interpolation.interp_scheme_2d module test
	"""
	return ["vice.toolkit.interpolation.interp_scheme_2d",
		[
			test_initialize(),
			test_attributes(),
			test_call()
		]
	]


@unittest
def test_initialize():
	r"""
	vice.toolkit.interpolation.interp_scheme_2d.__init__ unit test
	"""
	def test():
		try:
			test_ = interp_scheme_2d(_TEST_X_VALUES_, _TEST_Y_VALUES_,
				_TEST_Z_VALUES_)
		except:
			return False
		return isinstance(test_, interp_scheme_2d)
	return ["vice.toolkit.interpolation.interp_scheme_2d.__init__", test]


@unittest
def test_attributes():
	r"""
	vice.toolkit.interpolation.interp_scheme_2d attributes unit test
	"""
	def test():
		try:
			test_ = interp_scheme_2d(_TEST_X_VALUES_, _TEST_Y_VALUES_,
				_TEST_Z_VALUES_)
		except:
			return None
		status = isinstance(test_.xcoords, list)
		status &= isinstance(test_.ycoords, list)
		status &= isinstance(test_.zcoords, list)
		status &= test_.xcoords == _TEST_X_VALUES_
		status &= test_.ycoords == _TEST_Y_VALUES_
		status &= test_.zcoords == _TEST_Z_VALUES_
		status &= test_.n_x_values == len(_TEST_X_VALUES_)
		status &= test_.n_y_values == len(_TEST_Y_VALUES_)
		return status
	return ["vice.toolkit.interpolation.interp_scheme_2d.attributes", test]


@unittest
def test_call():
	r"""
	vice.toolkit.interpolation.interp_scheme_2d.__call__ unit test
	"""
	def test():
		try:
			test_ = interp_scheme_2d(_TEST_X_VALUES_, _TEST_Y_VALUES_,
				_TEST_Z_VALUES_)
		except:
			return None
		status = True
		random.seed()
		for i in range(1000):
			# based on the test coordinates defined above, f(x, y) = x + y
			# should always be the case. This should be the case for all
			# interpolated values as well, accounting for some small roundoff
			# error slightly above double precision.
			x = 200 * random.random() - 50 # between -50 and +150
			y = 300 * random.random() - 50 # between -50 and +250
			if x + y:
				percent_difference = abs(x + y - test_(x, y)) / (x + y)
			else:
				continue # prevents ZeroDivisionError
			status &= percent_difference < 1.e-14
			if not status: break
		return status
	return ["vice.toolkit.interpolation.interp_scheme_2d.__call__", test]


