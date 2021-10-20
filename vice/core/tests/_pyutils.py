
from __future__ import absolute_import
from ...testing import moduletest
from ...testing import unittest
from .._pyutils import numeric_check
from .._pyutils import inf_nan_check
from .._pyutils import copy_array_like_object
from .._pyutils import range_
from .._pyutils import args
from .._pyutils import arg_count
from .._pyutils import is_ascii
try:
	ModuleNotFoundError
except NameError:
	ModuleNotFoundError = ImportError
try:
	# NumPy compatible but not NumPy dependent
	import numpy as np
except (ModuleNotFoundError, ImportError):
	pass
try:
	# Pandas compatible but not Pandas dependent
	import pandas as pd
except:
	pass
import array
import sys


@moduletest
def test():
	r"""
	vice.core._pyutils module test
	"""
	return ["vice.core._pyutils",
		[
			test_numeric_check(),
			test_inf_nan_check(),
			test_copy_array_like_object(),
			test_range_(),
			test_args(),
			test_arg_count(),
			test_is_ascii()
		]
	]


@unittest
def test_numeric_check():
	r"""
	vice.core._pyutils.numeric_check unit test
	"""
	def test():
		test_ = list(range(100))
		status = True
		try:
			numeric_check(test_, TypeError, "Failed")
		except:
			status = False
		test_[50] = "test"
		try:
			numeric_check(test_, TypeError, "Failed")
		except TypeError:
			status &= True
		except:
			status = False
		return status
	return ["vice.core._pyutils.numeric_check", test]


@unittest
def test_inf_nan_check():
	r"""
	vice.core._pyutils.inf_nan_check unit test
	"""
	def test():
		test_ = list(range(100))
		status = True
		try:
			inf_nan_check(test_, TypeError, "Failed")
		except:
			status = False
		test_[50] = float("inf")
		test_[51] = float("nan")
		try:
			inf_nan_check(test_, TypeError, "Failed")
		except TypeError:
			status &= True
		except:
			status = False
		return status
	return ["vice.core._pyutils.inf_nan_check", test]


@unittest
def test_copy_array_like_object():
	r"""
	vice.core._pyutils.copy_array_like_object unit test
	"""
	def test():
		test_ = list(range(100))
		status = True
		x = copy_array_like_object(array.array('b', test_))
		status &= isinstance(x, list)
		status &= x == test_
		if "numpy" in sys.modules:
			x = copy_array_like_object(np.array(test_))
			status &= isinstance(x, list)
			status &= x == test_
		else: pass
		if "pandas" in sys.modules:
			x = copy_array_like_object(pd.DataFrame(test_))
			status &= isinstance(x, list)
			status &= x == test_
		else: pass
		return status
	return ["vice.core._pyutils.copy_array_like_object", test]


@unittest
def test_range_():
	r"""
	vice.core._pyutils.range_ unit test
	"""
	def test():
		test_ = range_(0, 100, 0.1)
		status = len(test_) == 1001
		n = 0
		while status and n < len(test_):
			status &= test_[n] == n * 0.1
			n += 1
		status &= test_[-1] >= 100
		return status
	return ["vice.core._pyutils.range_", test]


@unittest
def test_args():
	r"""
	vice.core._pyutils.args unit test
	"""
	def test():
		dummy = lambda x: 0.1 * x
		try:
			args(dummy, "Failed")
		except:
			return False
		dummy = lambda x, y: 0.1 * x * y
		try:
			args(dummy, "Failed")
		except TypeError:
			return True
		except:
			return False
	return ["vice.core._pyutils.args", test]


@unittest
def test_arg_count():
	r"""
	vice.core._pyutils.arg_count unit test
	"""
	def test():
		dummy = lambda x: 0.1 * x
		status = arg_count(dummy) == 1
		dummy = lambda x, y: 0.1 * x * y
		status &= arg_count(dummy) == 2
		dummy = lambda x, y, z: 0.1 * x * y * z
		status &= arg_count(dummy) == 3
		return status
	return ["vice.core._pyutils.arg_count", test]


@unittest
def test_is_ascii():
	r"""
	vice.core._pyutils.is_ascii unit test
	"""
	def test():
		return is_ascii("test") and not is_ascii(chr(129))
	return ["vice.core._pyutils.is_ascii", test]

