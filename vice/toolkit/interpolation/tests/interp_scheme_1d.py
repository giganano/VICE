
from __future__ import absolute_import
from ....testing import moduletest
from ....testing import unittest
from ..interp_scheme_1d import interp_scheme_1d
import random


@moduletest
def test():
	r"""
	vice.toolkit.interpolation.interp_scheme_1d module test
	"""
	return ["vice.toolkit.interpolation.interp_scheme_1d",
		[
			test_initialize(),
			test_attributes(),
			test_call(),
			test_getitem()
		]
	]


@unittest
def test_initialize():
	r"""
	vice.toolkit.interpolation.interp_scheme_1d.__init__ unit test
	"""
	def test():
		try:
			test_ = interp_scheme_1d([0, 1, 2], [0, 1, 2])
		except:
			return False
		return isinstance(test_, interp_scheme_1d)
	return ["vice.toolkit.interpolation.interp_scheme_1d.__init__", test]


@unittest
def test_attributes():
	r"""
	vice.toolkit.interpolation.interp_scheme_1d attributes unit test
	"""
	def test():
		try:
			test_ = interp_scheme_1d([0, 1, 2], [0, 1, 2])
		except:
			return None
		status = isinstance(test_.xcoords, list)
		status &= isinstance(test_.ycoords, list)
		status &= test_.xcoords == test_.ycoords == [0, 1, 2]
		status &= len(test_.xcoords) == test_.n_points == 3
		return status
	return ["vice.toolkit.interpolation.interp_scheme_1d.attributes", test]


@unittest
def test_call():
	r"""
	vice.toolkit.interpolation.interp_scheme_1d.__call__ unit test
	"""
	def test():
		try:
			test_ = interp_scheme_1d(list(range(-50, 50)), list(range(-50, 50)))
		except:
			return None
		status = True
		for i in range(1000):
			x = 200 * random.random() - 100 # between -100 and +100
			status &= test_(x) == x
			if not status: break
		return status
	return ["vice.toolkit.interpolation.interp_scheme_1d.__call__", test]


@unittest
def test_getitem():
	r"""
	vice.toolkit.interpolation.interp_scheme_1d.__getitem__ unit test
	"""
	def test():
		try:
			test_ = interp_scheme_1d([0, 1, 2], [0, 1, 2])
		except:
			return None
		status = test_[0] == [0.0, 0.0]
		status &= test_[1] == [1.0, 1.0]
		status &= test_[2] == [2.0, 2.0]
		status &= test_[0:2] == [[0.0, 0.0], [1.0, 1.0]]
		status &= test_[0:3] == [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]]
		return status
	return ["vice.toolkit.interpolation.interp_scheme_1d.__getitem__", test]

