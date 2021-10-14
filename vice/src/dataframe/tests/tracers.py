
from __future__ import absolute_import
__all__ = ["test_tracers_row"]
from ....testing import unittest
from ....core.dataframe import base
from ....core.outputs import stars
import numbers
import random


@unittest
def test_tracers_row():
	r"""
	vice.core.dataframe.tracers.__getitem__.row unit test
	"""
	def test():
		r"""
		This funciton will only be called after the test.vice multizone output
		has been produced by the module test which calls this.
		"""
		try:
			_TEST_ = stars("test")
		except:
			return False
		status = True
		random.seed()
		for _ in range(10):
			# Testing every single row of the stars object is too
			# computationally expensive for a test - it chews up gigabytes
			# of data that can only be freed by restarting the python
			# interpreter since it's captured in python here. Instead, draw
			# ten rows at random and test them individually, then move on.
			idx = int(_TEST_.size[0] * random.random())
			status &= isinstance(_TEST_[idx], base)
			status &= _TEST_[idx].keys() == _TEST_.keys()
			status &= all([isinstance(i, numbers.Number) for i in
				[_TEST_[idx][j] for j in _TEST_.keys()]])
			if not status: break
			# assert isinstance(_TEST_[i], base)
			# assert _TEST_[i].keys() == _TEST_.keys()
			# assert all(map(lambda x: isinstance(x, numbers.Number),
			# 	[_TEST_[i][j] for j in _TEST_.keys()]))
		return status
	return ["vice.core.dataframe.tracers.__getitem__.row", test]

