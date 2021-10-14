
from __future__ import absolute_import
__all__ = ["test_history_row"]
from ....testing import unittest
from ....core.dataframe import base
from ....core.outputs import history
import numbers
import random


@unittest
def test_history_row():
	r"""
	vice.core.dataframe.history.__getitem__.row unit test
	"""
	def test():
		r"""
		This function will only be called after the test.vice singlezone
		output has been produced by the module test which calls this.
		"""
		try:
			_TEST_ = history("test")
		except:
			return False
		status = True
		random.seed()
		# Testing every single row of the history object is too computationally
		# expensive for a test - it chews up gigabytes of data that can only be
		# freed by restarting the python interpreter since it's captured in
		# python here. Instead, draw ten rows at random and test them
		# individually, then move on.
		for _ in range(10):
			idx = int(_TEST_.size[0] * random.random())
			status &= isinstance(_TEST_[idx], base)
			status &= _TEST_[idx].keys() == _TEST_.keys()
			status &= all([isinstance(i, numbers.Number) for i in
				[_TEST_[idx][j] for j in _TEST_.keys()]])
			if not status: break
		return status
	return ["vice.core.dataframe.history.__getitem__.row", test]

