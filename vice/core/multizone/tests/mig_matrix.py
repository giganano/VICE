r"""
This file implements testing of the migration_matrix object in _migration.pyx
"""

from __future__ import absolute_import
__all__ = ["test"]
from .._migration import mig_matrix_row
from .._migration import mig_matrix
from ....testing import moduletest
from ....testing import unittest
import numbers
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError

# The size of the test matrix
_TEST_SIZE_ = 10


@moduletest
def test():
	r"""
	mig_matrix module test
	"""
	return ["vice.core.multizone.migration.mig_matrix",
		[
			test_initialization(),
			test_getitem(),
			test_setitem(),
			test_size(),
			test_tolist(),
			test_tonumpyarray()
		]
	]


@unittest
def test_initialization():
	r"""
	Initialization unit test
	"""
	def test():
		global _TEST_
		try:
			_TEST_ = mig_matrix(_TEST_SIZE_)
		except:
			return False
		return isinstance(_TEST_, mig_matrix)
	return ["vice.core.multizone.migration.mig_matrix.__init__", test]


@unittest
def test_getitem():
	r"""
	__getitem__ unit test
	"""
	def test():
		try:
			for i in range(_TEST_SIZE_):
				assert isinstance(_TEST_[i], mig_matrix_row)
				assert _TEST_[i].size == _TEST_SIZE_
		except:
			return False
		return True
	return ["vice.core.multizone.migration.mig_matrix.__getitem__", test]


@unittest
def test_setitem():
	r"""
	__setitem__ unit test
	"""
	def test():
		try:
			for i in range(_TEST_SIZE_):
				for j in range(_TEST_SIZE_):
					_TEST_[i, j] = 1.
					assert _TEST_[i, j] == 1.
					_TEST_[i, j] = dummy
					assert _TEST_[i, j] == dummy
		except:
			return False
		for i in range(_TEST_SIZE_):
			for j in range(_TEST_SIZE_):
				_TEST_[i, j] = 0.
		return True
	return ["vice.core.multizone.migration.mig_matrix.__setitem__", test]


@unittest
def test_size():
	r"""
	size property unit test
	"""
	def test():
		return _TEST_.size == _TEST_SIZE_
	return ["vice.core.multizone.migration.mig_matrix.size", test]


@unittest
def test_tolist():
	r"""
	tolist function unit test
	"""
	def test():
		try:
			x = _TEST_.tolist()
		except:
			return False
		return isinstance(x, list) and x == _TEST_SIZE_ * [_TEST_SIZE_ * [0.]]
	return ["vice.core.multizone.migration.mig_matrix.tolist", test]


@unittest
def test_tonumpyarray():
	r"""
	tonumpyarray unit test
	"""
	def test():
		try:
			import numpy as np
		except (ModuleNotFoundError, ImportError):
			return
		try:
			x = _TEST_.tonumpyarray()
		except (ModuleNotFoundError, ImportError):
			return
		except:
			return False
		return (isinstance(x, np.ndarray) and
			all(map(lambda y: all(np.equal(y, _TEST_SIZE_ * [0.])), x)))
	return ["vice.core.multizone.migration.mig_matrix.tonumpyarray", test]


def dummy(t):
	r"""
	A dummy function of time
	"""
	return 1.

