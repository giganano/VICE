r"""
Callback object unit tests
"""

from __future__ import absolute_import
__all__ = ["test"]
from ...testing import moduletest
from ...testing import unittest
from ..callback import numerical
from ..callback import no_nan
from ..callback import no_inf
from ..callback import positive
from ..callback import callback1
from ..callback import callback1_nan
from ..callback import callback1_nan_inf
from ..callback import callback1_nan_positive
from ..callback import callback1_nan_inf_positive
from ..callback import callback2
from ..callback import callback2_nan
from ..callback import callback2_nan_inf
from ..callback import callback2_nan_positive
from ..callback import callback2_nan_inf_positive


@moduletest
def test():
	r"""
	vice.core.callback module test
	"""
	return ["vice.core.callback",
		[
			test_numerical(),
			test_no_nan(),
			test_no_inf(),
			test_positive(),
			test_callback1(),
			test_callback1_nan(),
			test_callback1_nan_inf(),
			test_callback1_nan_positive(),
			test_callback1_nan_inf_positive(),
			test_callback2(),
			test_callback2_nan(),
			test_callback2_nan_inf(),
			test_callback2_nan_positive(),
			test_callback2_nan_inf_positive()
		]
	]


@unittest
def test_numerical():
	r"""
	vice.core.callback.numerical unit test
	"""
	def test():
		@numerical
		def dummy(x):
			if x:
				return 1
			else:
				return "foo"
		return dummy(1) == 1 and dummy(0) == 0
	return ["vice.core.callback.numerical", test]


@unittest
def test_no_nan():
	r"""
	vice.core.callback.no_nan unit test
	"""
	def test():
		@no_nan
		def dummy(x):
			if x:
				return 1
			else:
				return float("nan")
		return dummy(1) == 1 and dummy(0) == 0
	return ["vice.core.callback.no_nan", test]


@unittest
def test_no_inf():
	r"""
	vice.core.callback.no_inf unit test
	"""
	def test():
		@no_inf
		def dummy(x):
			if x:
				return 1
			else:
				return float("inf")
		return dummy(1) == 1 and dummy(0) == 0
	return ["vice.core.callback.no_inf", test]


@unittest
def test_positive():
	r"""
	vice.core.callback.positive unit test
	"""
	def test():
		@positive
		def dummy(x):
			return x
		return dummy(1) == 1 and dummy(0) == 1e-12 and dummy(-1) == 1e-12
	return ["vice.core.callback.positive", test]


def dummy1(x):
	r"""
	A dummy function of one numerical value
	"""
	return 1 + x**2


def test_callback1_engine(cb):
	r"""
	Runs a callback1 object unit test.

	Parameters
	----------
	cb : ``callback1``
		A callback1 object.

	Returns
	-------
	result : ``bool``
		True if the callback object passes the test. False if it failed.
	"""
	return cb(0) == 1 and cb(1) == 2 and cb(2) == 5


@unittest
def test_callback1():
	r"""
	vice.core.callback.callback1 unit test
	"""
	def test():
		try:
			return test_callback1_engine(callback1(dummy1))
		except:
			return False
	return ["vice.core.callback.callback1", test]


@unittest
def test_callback1_nan():
	r"""
	vice.core.callback.callback1_nan unit test
	"""
	def test():
		try:
			return test_callback1_engine(callback1_nan(dummy1))
		except:
			return False
	return ["vice.core.callback.callback1_nan", test]


@unittest
def test_callback1_nan_inf():
	r"""
	vice.core.callback.callback1_nan_inf unit test
	"""
	def test():
		try:
			return test_callback1_engine(callback1_nan_inf(dummy1))
		except:
			return False
	return ["vice.core.callback.callback1_nan_inf", test]


@unittest
def test_callback1_nan_positive():
	r"""
	vice.core.callback.callback1_nan_positive unit test
	"""
	def test():
		try:
			return test_callback1_engine(callback1_nan_positive(dummy1))
		except:
			return False
	return ["vice.core.callback.callback1_nan_positive", test]


@unittest
def test_callback1_nan_inf_positive():
	r"""
	vice.core.callback.callback1_nan_inf_positive unit test
	"""
	def test():
		try:
			return test_callback1_engine(callback1_nan_inf_positive(dummy1))
		except:
			return False
	return ["vice.core.callback.callback1_nan_inf_positive", test]


def dummy2(x, y):
	return 1 + x * y


def test_callback2_engine(cb):
	r"""
	Runs a callback2 object unit test.

	Parameters
	----------
	cb : ``callback2``
		A callback2 object.

	Returns
	-------
	result : ``bool``
		True if the callback object passes the test. False if it failed.
	"""
	return cb(0, 0) == 1 and cb(1, 2) == 3 and cb(3, 2) == 7


@unittest
def test_callback2():
	r"""
	vice.core.callback.callback2 unit test
	"""
	def test():
		try:
			return test_callback2_engine(callback2(dummy2))
		except:
			return False
	return ["vice.core.callback.callback2", test]


@unittest
def test_callback2_nan():
	r"""
	vice.core.callback.callback2_nan unit test
	"""
	def test():
		try:
			return test_callback2_engine(callback2_nan(dummy2))
		except:
			return False
	return ["vice.core.callback.callback2_nan", test]


@unittest
def test_callback2_nan_inf():
	r"""
	vice.core.callback.callback2_nan_inf unit test
	"""
	def test():
		try:
			return test_callback2_engine(callback2_nan_inf(dummy2))
		except:
			return False
	return ["vice.core.callback.callback2_nan_inf", test]


@unittest
def test_callback2_nan_positive():
	r"""
	vice.core.callback.callback2_nan_positive unit test
	"""
	def test():
		try:
			return test_callback2_engine(callback2_nan_positive(dummy2))
		except:
			return False
	return ["vice.core.callback.callback2_nan_positive", test]


@unittest
def test_callback2_nan_inf_positive():
	r"""
	vice.core.callback.callback2_nan_inf_positive unit test
	"""
	def test():
		try:
			return test_callback2_engine(callback2_nan_inf_positive(dummy2))
		except:
			return False
	return ["vice.core.callback.callback2_nan_inf_positive", test]

